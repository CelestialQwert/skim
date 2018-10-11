import sys
import pygame

class Manager():

    def __init__(self):

        self.done = False
        self.screen = pygame.display.set_mode((640,480))
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.states = {
            "INTRO": Intro(),
            "DUMMYGAME": DummyGame()
        }

        self.state_name = 'INTRO'
        self.state = self.states[self.state_name]
        self.last_state = None

    def handle_events(self):
        for event in pygame.event.get():
            self.state.handle_event(event)

    def flip_state(self):            
        #shutdown old state
        persist = self.state.cleanup()
        self.state.done = False
        #switch to new state
        self.last_state = self.state_name
        self.state_name = self.state.next_state
        self.state = self.states[self.state_name]
        #startup new state
        self.state.startup(persist)

    def update(self,dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw_screen(self):
        self.state.draw_screen(self.screen)
        pygame.display.update()

    def main_loop(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt)
            self.draw_screen()

class State():

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

    def startup(self,persist):
        self.persist = persist

    def handle_event(self,event):
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self,dt):
        pass

    def draw_screen(self):
        pass

    def cleanup(self):
        return self.persist

class Intro(State):

    def __init__(self):
        super(Intro,self).__init__()
        self.title = self.font.render("Intro WOOOOO", True, pygame.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "DUMMYGAME"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True

    def draw_screen(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)  


class DummyGame(State):
    def __init__(self):
        super(DummyGame, self).__init__()
        self.rect = pygame.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        
    def startup(self, persist):
        self.persist = persist
        color = self.persist["screen_color"]
        self.screen_color = pygame.Color(color)
        if color == "dodgerblue":
            text = "You clicked the mouse to get here"
        elif color == "gold":
            text = "You pressed a key to get here"
        self.title = self.font.render(text, True, pygame.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.title_rect.center = event.pos
        
    def update(self,dt):
        self.rect.move_ip(self.x_velocity, )
        if (self.rect.right > self.screen_rect.right
            or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)
                 
    def draw_screen(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.title, self.title_rect)
        pygame.draw.rect(surface, pygame.Color("darkgreen"), self.rect)


if __name__ == "__main__":
    pygame.init()
    game = Manager()
    game.main_loop()
    pygame.quit()
    sys.exit()