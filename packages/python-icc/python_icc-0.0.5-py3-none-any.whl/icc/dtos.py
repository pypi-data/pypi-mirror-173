from pydantic import BaseModel


class LightingRequest(BaseModel):
    target: str
    operation: str


class HsvRequest(LightingRequest):
    h: int = 0
    s: int = 100
    v: int = 50


class BrightnessRequest(LightingRequest):
    brightness: int


class TemperatureRequest(LightingRequest):
    temperature: str
