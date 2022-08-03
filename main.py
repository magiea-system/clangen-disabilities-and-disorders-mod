import sys

from scripts.screens import *

# P Y G A M E
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load('resources/icon.png'))

# LOAD cats & clan
with open('saves/clanlist.txt', 'r') as read_file:
    clan_list = read_file.read()
    if_clans = len(clan_list)
if if_clans > 0:
    game.switches['clan_list'] = clan_list.split('\n')
    cat_class.load_cats()
    clan_class.load_clan()
# LOAD settings
game.load_settings()

# give thoughts/actions to already existing cats
cat_class.thoughts()

while True:
    screen.fill((255, 255, 255))
    # background
    # bg = pygame.image.load("resources/menu.png")
    # bg = pygame.transform.scale(bg, (1000,500))
    # screen.blit(bg, (0,0))
    mouse.check_pos()

    # EVENTS
    for event in pygame.event.get():
        if game.current_screen == 'make clan screen' and game.switches[
            'clan_name'] == '':  # Allows user to type in Clan Name
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():  # only allows alphabet letters as an input
                    if len(game.switches['naming_text']) < game.max_name_length:  # can't type more than max name length
                        game.switches['naming_text'] += event.unicode
                elif event.key == pygame.K_BACKSPACE:  # delete last character of clan name
                    game.switches['naming_text'] = game.switches['naming_text'][:-1]

        if game.current_screen == 'events screen' and len(game.cur_events_list) > game.max_events_displayed:
            max_scroll_direction = len(game.cur_events_list) - game.max_events_displayed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.event_scroll_ct < 0:
                    game.cur_events_list.insert(0, game.cur_events_list.pop())
                    game.event_scroll_ct += 1
                if event.key == pygame.K_DOWN and abs(game.event_scroll_ct) < max_scroll_direction:
                    game.cur_events_list.append(game.cur_events_list.pop(0))
                    game.event_scroll_ct -= 1
        if event.type == pygame.QUIT:
            # close pygame
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.clicked = True

    # SCREENS
    game.all_screens[game.current_screen].on_use()

    # update
    game.update_game()
    if game.switch_screens:
        screens.all_screens[game.current_screen].screen_switches()
        game.switch_screens = False
    # END FRAME
    clock.tick(60)

    pygame.display.update()
