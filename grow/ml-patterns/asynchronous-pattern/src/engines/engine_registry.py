from src.engines.base.model_manager import ModelManager

engine_manager = ModelManager()

engine_manager.load_model("src.engines.background_removal.inference.BackgroundRemoval")
