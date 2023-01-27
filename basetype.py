
from pydantic import BaseModel
from typing import List
from typing_extensions import TypedDict

class Masker(TypedDict):
    seed: int
    mask: str
    
class GenerationOutput(BaseModel):
    output: List[str]
    

class GenerationRequest(BaseModel):
    prompt: str
    image: str = None
    n_samples: int = 1
    steps: int = 50
    sampler: str = "DDIM"
    fixed_code: bool = False
    ddim_eta: float = 0.0
    height: int = 512
    width: int = 512
    latent_channels: int = 4
    downsampling_factor: int = 8
    scale: float = 7.0
    dynamic_threshold: float = None
    seed: int = None
    temp: float = 1.0
    top_k: int = 256
    grid_size: int = 4
    advanced: bool = False
    stage_two_seed: int = None
    strength: float = 0.69
    noise: float = 0.667
    mitigate: bool = False
    module: str = None
    masks: List[Masker] = None
    uc: str = None