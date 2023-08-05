import sdl2.ext
from shikkoku.app import App
from shikkoku.sample_scene import SampleScene

def main():
    """Main game entry point."""
    
    with App("Game", (1200, 800)) as app:
        app.assign_resource_path("shikkoku.resources")
        scene = SampleScene(app, "test")
        app.add_scene(scene)
        
        app.start_game_loop(scene)
    
main()