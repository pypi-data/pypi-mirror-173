from .lib import *
from .third_party.yolov5.utils.plots import Annotator as _Annotator
from colorsys import hsv_to_rgb

__all__ = ['pil2tensor', 'tensor2pil', 'tensor2ndarray', 'ndarray2tensor', 'read_img', 'write_img', 
           'Annotator', 'ValidPad']

pil2tensor = tv.transforms.ToTensor()
tensor2pil = tv.transforms.ToPILImage()


def tensor2ndarray(img: Union[torch.Tensor, List[torch.Tensor]]) -> np.ndarray:
    """Convert torch tensor to opencv ndarray.
    1. The color space is from RGB to BGR.
    2. The pixel value is from [0., 1.] to [0, 255].
    3. Valid input: 3-dim [c, h, w] or 4-dim [b, c, h, w]
    4. Case 1: [c, h, w] or [1, c, h, w] -> [h, w, c] 
    5. Case 2: [b, c, h, w] -> [b, h, w, c] 
    """
    if isinstance(img, list):
        if len(img) == 1:
            return tensor2ndarray(img[0])
        else:
            return tensor2ndarray(torch.stack(img))
    elif isinstance(img, torch.Tensor):
        img = img.mul(255).cpu().detach()
        if img.ndim == 4 and img.shape[0] == 1:
            img = img[0]
        if img.ndim == 3:
            img = img.permute(1, 2, 0)
        elif img.ndim == 4:
            img = img.permute(0, 2, 3, 1)
        else:
            raise NotImplementedError
        img2: np.ndarray = img.numpy()
        img2 = np.ascontiguousarray(img2.astype(np.uint8)[..., ::-1])
    else:
        raise NotImplementedError
    return img2


def ndarray2tensor(img: Union[np.ndarray, List[np.ndarray]]) -> torch.Tensor:
    """Convert opencv ndarray to torch tensor.
    1. The color space is from BGR to RGB.
    2. The pixel value is from [0, 255] to [0., 1.].
    3. Valid input: 3-dim [h, w, c] or 4-dim [b, h, w, c]
    4. Case 1: [h, w, c] -> [1, c, h, w]
    5. Case 2: [b, h, w, c] -> [b, c, h, w] 
    """
    if isinstance(img, list):
        if len(img) == 1:
            return tensor2ndarray(img[0])
        else:
            return tensor2ndarray(np.stack(img, axis=0))
    elif isinstance(img, np.ndarray):
        img = img.astype(np.float32) / 255
        img = np.ascontiguousarray(img[..., ::-1])
        img2: torch.Tensor = torch.from_numpy(img)
        if img2.ndim == 4:
            img2 = img2.permute(0, 3, 1, 2)
        elif img2.ndim == 3:
            img2 = img2.permute(2, 0, 1).unsqueeze(0)
        else:
            raise NotImplementedError
        img2 = img2.contiguous()
    else:
        raise NotImplementedError
    return img2


def read_img(path: str) -> torch.Tensor:
    return pil2tensor(Image.open(path).convert("RGB")).unsqueeze(0)


def write_img(img: torch.Tensor, path: str):
    tv.utils.save_image(img, path)


class Annotator(_Annotator):
    def __init__(self, im, line_width=None, font_size=None, font='Arial.ttf', pil=False, example='abc'):
        im = tensor2ndarray(im) if isinstance(im, torch.Tensor) else np.ascontiguousarray(im)
        super().__init__(im, line_width, font_size, font, pil, example)
        self.colorset = [
            (int(r*255), int(g*255), int(b*255)) for k in range(80) 
                for r, g, b in [hsv_to_rgb((k%20)/20, 0.5+(k//20)/8, 0.5+(k//20)/8)]
        ]
        random.seed(0)
        random.shuffle(self.colorset)
    
    def box_label(self, box, label, idx):
        color = self.colorset[idx]
        txt_color = (255, 255, 255)
        return super().box_label(box, label, color, txt_color)
    
    def box_label_all(self, pred):
        for *box, conf, cls in pred:
            cls = int(cls.item())
            conf = float(conf.item())
            label = f"{cls} {conf:.2f}"
            self.box_label(box, label, cls)

    def save(self, path):
        img = self.result()
        cv2.imwrite(path, img)


class ValidPad:
    def __init__(self, base=64) -> None:
        self.base = base
    
    def __call__(self, x:torch.Tensor) -> torch.Tensor:
        nc = x.shape[:-2]
        h, w = x.shape[-2:]
        h2 = (h+self.base-1)//self.base*self.base
        w2 = (w+self.base-1)//self.base*self.base
        x2 = torch.ones((*nc, h2, w2), device=x.device, dtype=x.dtype)
        x2[..., :h, :w] = x
        return x2
