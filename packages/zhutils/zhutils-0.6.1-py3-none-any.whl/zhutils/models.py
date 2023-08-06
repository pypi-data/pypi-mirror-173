from .lib import *
from .third_party.yolov5.models.yolo import attempt_load, non_max_suppression
from .third_party.yolov5.utils.loss import ComputeLoss
from .third_party.facenet import MTCNN
from .third_party.facenet import InceptionResnetV1 as IResnet
from .third_party.facerecog import *
from .utils import ValidPad

__all__ = ['YOLOv5', 'YOLOv5B', 'MTCNN', 'IResnet', 'FaceRecogModel']


class YOLOv5:
    def __init__(self, device, conf_thres: float = 0.25, varient: str = "m"):
        if not os.path.exists("weights"):
            os.makedirs("weights")
        assert varient in ["n", "s", "m", "l", "x"]
        self.model = attempt_load(f"weights/yolov5{varient}.pt",
                                  map_location=device,
                                  fuse=True).eval()
        for k in self.model.model.children():
            if "Detect" in str(type(k)):
                k.inplace = False
        self.conf_thres = conf_thres
        self.pad = ValidPad(32)
        self.nms = lambda x: non_max_suppression(x, conf_thres=self.conf_thres)
        self.compute_loss = ComputeLoss(self.model)

    def __call__(self, x:torch.Tensor, eval=True, roi=None):
        x = self.pad(x)
        if eval:
            with torch.no_grad():
                pred = self.model(x)[0]
                ret = self.nms(pred)
            if roi is not None:
                roi = set([roi] if isinstance(roi, int) else roi)
                tmp = []
                for ret_i in ret:
                    tmp_i = []
                    for y in ret_i:
                        if int(y[-1]) in roi:
                            tmp_i.append(y)
                    if len(tmp_i):
                        tmp.append(torch.stack(tmp_i))
                    else:
                        tmp.append(torch.empty((0, 6), device=x.device))
                ret = tmp
        else:
            ret = self.model(x)[0]
        return ret


class YOLOv5B:
    def __init__(self, device, conf_thres: float = 0.25, varient: str = "m"):
        if not os.path.exists("weights"):
            os.makedirs("weights")
        assert varient in ["n", "s", "m", "l", "x"]
        self.model = attempt_load(f"weights/yolov5{varient}.pt",
                                  map_location=device,
                                  fuse=True).eval()
        self.conf_thres = conf_thres
        self.resize = tv.transforms.Resize((640, 640))
        self.nms = lambda x: non_max_suppression(x, conf_thres=self.conf_thres)

    @torch.no_grad()
    def __call__(self, x:Union[torch.Tensor, List[torch.Tensor]], roi=None):
        if isinstance(x, list):
            h_before = torch.tensor([xi.shape[-2] for xi in x])
            w_before = torch.tensor([xi.shape[-1] for xi in x])
            x = torch.stack([self.resize(xi).squeeze() for xi in x])
        else:
            h_before = torch.ones(x.shape[0]) * x.shape[-2]
            w_before = torch.ones(x.shape[0]) * x.shape[-1]
            x = self.resize(x)
        pred = self.model(x)[0]
        ret = self.nms(pred)

        h_ratio = h_before.type_as(x).to(x.device).div(640)
        w_ratio = w_before.type_as(x).to(x.device).div(640)
        ratio = torch.stack([w_ratio, h_ratio, w_ratio, h_ratio], dim=1).unsqueeze(1)
        for ret_i, ratio_i in zip(ret, ratio):
            ret_i[:, :4] *= ratio_i

        if roi is not None:
            roi = set([roi] if isinstance(roi, int) else roi)
            tmp = []
            for ret_i in ret:
                tmp_i = []
                for y in ret_i:
                    if int(y[-1]) in roi:
                        tmp_i.append(y)
                if len(tmp_i):
                    tmp.append(torch.stack(tmp_i))
                else:
                    tmp.append(torch.empty((0, 6), device=x.device))
            ret = tmp
        return ret



class FaceRecogModel:
    def __init__(self, device, varient="facenet") -> None:
        if varient == "facenet":
            self.net = InceptionResnetV1(pretrained="vggface2", device=device)
        elif varient == "mobile":
            self.net = MobileFaceNet(512).to(device)
        elif varient == "ir152":
            self.net = IR_152((112, 112)).to(device)
        elif varient == "irse50":
            self.net = IR_SE_50((112, 112)).to(device)
        self.input_size = (112, 112)
        
        url = "https://github.com/forget2save/zhutils/releases/download/Models2"
        weights = f"weights/{varient}.pth"
        if not os.path.exists(weights):
            if not os.path.exists(os.path.dirname(weights)):
                os.makedirs(os.path.dirname(weights))
            torch.hub.download_url_to_file(f"{url}/{varient}.pth", weights)
        self.net.load_state_dict(torch.load(weights, map_location=device))
        self.net.eval()

    def __call__(self, x:torch.Tensor, norm=True) -> Any:
        y = self.resize(x)
        z = self.net(2*y-1)
        if norm:
            z = self.l2_norm(z)
        return z
    
    def resize(self, x:torch.Tensor) -> torch.Tensor:
        assert x.ndim == 4
        return F.interpolate(x, self.input_size, mode="area")
    
    def l2_norm(self, input:torch.Tensor, axis=1):
        norm = torch.norm(input, 2, axis, True)
        output = torch.div(input, norm)
        return output

