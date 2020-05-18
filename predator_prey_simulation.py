# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:47:59 2020
Finished on 5/17/2020

@author: smika
"""

def predator_prey_activity(interactive=True, blind_folded = True, prey_distribtion = '', environment_complexity = ''):    #mute pygame startup prompt
    #remove the startup message
    import os
    import datetime
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    
    
    #import pygame and my modules
    import pygame
    from lib.grid import Grid
    from lib.sprite import Sprite
    
    #global list of supported types
    TYPES_OF_PREY_DIST = ['even','random','clumped']
    TYPES_OF_ENV_COMP = ['simple','moderate','complex']
    
    #if you run this as predator_prey_activity(False) you can get terminal assignment of simulation type
    #this is skipped when the next two parameters are filled or if they want it interactive
    if (prey_distribtion == '' or environment_complexity == '') and not interactive:
        
        # get user input
        prey_distribtion = input("Enter Prey Distribution Selection (Options:" + str(TYPES_OF_PREY_DIST) + "): ")
        environment_complexity = input("Enter Enviroment Complexity Selection (Options:" + str(TYPES_OF_ENV_COMP) + "): ")
        
        #if they skip past it, then assign a default
        if prey_distribtion == '':
            prey_distribtion = 'random'
        if environment_complexity == '':
            environment_complexity == 'moderate'
            
        print(f'Running Simulation using a(n) {prey_distribtion} prey distribution and a {environment_complexity} enviornment complexity. ')
    
    
    #initialize pygame and ensure all packages
    pygame.init()
    pygame.font.init()
    
    #title the window
    pygame.display.set_caption("Predatory Prey Simulation")
    
    #variables for running loops
    run = True #main game loop
    count_down = 3 #the seconds to wait before the game starts
    delay = 200 #how long the main game loops waits each iteration to feel natural
    time = 0 # this is a display variabe
    max_time = 60
    
        
    #play again flags
    play_again = False
    selected = False
    
    #for start button
    start_pressed = False
    
    
    #create some assorted sized fonts for typing
    bigfont = pygame.font.SysFont(None, 40)
    mfont = pygame.font.SysFont(None, 30)
    font = pygame.font.SysFont(None, 20)
    
    #create our window
    game_window_width = 1000
    game_window_height = 750
    game_window_size = (game_window_width,game_window_height)
    game_window = pygame.display.set_mode(game_window_size)
    
    #how much of the right half of the screen is the HUD's
    HUD_scale = 0.25
    
    #colors for the backgrounds and to remove magic numbers
    simulation_background_color = (51,51,51)
    highlighted_color = (101,101,101)
    HUD_background_color = (151,151,151)
    color_black = (0,0,0)
    
    # here is the offset of the choice box
    choice_offset = game_window_width/50
    
    #text for descriptions
    prey_dist_text = bigfont.render('Prey Distributions', True, color_black)
    env_type_text = bigfont.render('Enviroment Complexities', True, color_black)
    start_text = bigfont.render('Start', True, color_black)
    
    #text for prey dist choice box & container
    even_text = bigfont.render('EVEN', True, color_black)
    random_text = bigfont.render('RANDOM', True, color_black)
    clumped_text = bigfont.render('CLUMPED', True, color_black)
    prey_text_options = [even_text, random_text, clumped_text]
    
    #text for env dist choice box & container
    simple_text = bigfont.render('SIMPLE', True, color_black)
    moderate_text = bigfont.render('MODERATE', True, color_black)
    complex_text = bigfont.render('COMPLEX', True, color_black)
    env_text_options = [simple_text, moderate_text, complex_text]
    
    #text for env dist choice box & container
    play_again_text = bigfont.render('Play Again?', True, color_black)
    play_nomore = bigfont.render('Exit', True, color_black)
    save_to_file = bigfont.render('Save Results', True, color_black)
    saved_to = font.render('', True, color_black)
    game_over = mfont.render('Simulation Complete', True, color_black)
    
    #varible for the mouse locationfor choice box
    mouse_pos = (-1,-1)  

    #let them see distribution for a second      
    peek = 500
    
    #the onscreen startup text and images
    image_1 = pygame.image.load('lib/supported_input.png')
    intro_1 = bigfont.render('Predator Prey Simulation!', True, color_black)
    intro_2 = mfont.render('This simulation was made to model real life predator, prey, and eviornment relationships!', True, color_black)
    intro_3 = mfont.render('Here is the list of supported prey distributions and enviornment complexities:', True, color_black)
    intro_4 = mfont.render('The simulation will ask for each of these as inputs seperately, and after a countdown start it', True, color_black)
    intro_3 = mfont.render('If \'blindfolded\' the prey will only show for ' + str(peek/1000) + " seconds.", True, color_black)
    intro_5 = mfont.render('Use the arrow keys to overlap the red predator square with the white prey square to kill it', True, color_black)
    intro_6 = mfont.render('Avoid black obstacles, get as many as possible in 60 seconds, record the kills!', True, color_black)
    intro_text = [intro_1, intro_2, intro_3, intro_4, intro_5, intro_6]
    intro_text.append(image_1)

    
    #start the intro
    intro = True
    while intro:
        pygame.time.delay(delay)
        #event handling like skipping everything v just the intro
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                intro = False
                selected = True
                prey_distribtion = '-1'
                environment_complexity = '-1'
                count_down = -1
                start_pressed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro = False
        #background
        pygame.draw.rect(game_window, HUD_background_color, (0,0,game_window_width,game_window_height ) )
        #draw each element in the intro_text container 
        for i, element in enumerate(intro_text):
            game_window.blit(element, (50, i*25+25))
        #draw the screen
        pygame.display.update()
        
    #if at this point the prey distribution etc isnt picked then i assume we need it and want it graphically
    prey_colors = [HUD_background_color,HUD_background_color,HUD_background_color]
    env_colors = [HUD_background_color,HUD_background_color,HUD_background_color]
    
    while not start_pressed:
        pygame.time.delay(delay)
        
        #check for program exit and mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                selected = True
                prey_distribtion = '-1'
                environment_complexity = '-1'
                count_down = -1
                start_pressed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
        #background
        pygame.draw.rect(game_window, simulation_background_color, (0, 0, game_window_width, game_window_height) )
        height = 200
        game_window.blit(prey_dist_text, (choice_offset,choice_offset))
        game_window.blit(env_type_text, (choice_offset,14*choice_offset))
        for o in range(3):
            pygame.draw.rect(game_window, prey_colors[o], ((game_window_width/3*o)+2*choice_offset,3*choice_offset,game_window_width/3-3*choice_offset, height) )
            game_window.blit(prey_text_options[o], ((game_window_width/3*o)+2*choice_offset,3*choice_offset))
            
            pygame.draw.rect(game_window, env_colors[o], ((game_window_width/3*o)+2*choice_offset,height+6*choice_offset,game_window_width/3-3*choice_offset, height) )
            game_window.blit(env_text_options[o], ((game_window_width/3*o)+2*choice_offset,height+6*choice_offset))
        
        pygame.draw.rect(game_window, HUD_background_color, ((game_window_width/3*1)+2*choice_offset,2*height+8*choice_offset,game_window_width/3-3*choice_offset, height/2) )
        game_window.blit(start_text, ((game_window_width/3*1)+2*choice_offset,2*height+8*choice_offset))  
        for o in range(3):
            if mouse_pos[0] > (game_window_width/3*o)+2*choice_offset and mouse_pos[0] < (game_window_width/3*o)+2*choice_offset + game_window_width/3-3*choice_offset:
                if mouse_pos[1] < height + 3*choice_offset:
                    prey_colors = [HUD_background_color,HUD_background_color,HUD_background_color]
                    prey_colors[o] = highlighted_color
                    prey_distribtion = TYPES_OF_PREY_DIST[o]
                    mouse_pos = (-1,-1)
                elif mouse_pos[1] < 2*height + 6*choice_offset:
                    env_colors = [HUD_background_color,HUD_background_color,HUD_background_color]
                    env_colors[o] = highlighted_color
                    environment_complexity = TYPES_OF_ENV_COMP[o]
                    mouse_pos = (-1,-1)
        if mouse_pos[0] > (game_window_width/3*1)+2*choice_offset and mouse_pos[1] < (game_window_width/3*1)+2*choice_offset + game_window_width/3-3*choice_offset:
            if mouse_pos[1] > 2*height+8*choice_offset:
                if not (prey_distribtion == '' or environment_complexity == ''):
                    start_pressed = True
                    mouse_pos = (-1,-1)
        mouse_pos = (-1,-1)
        #update the screen
        pygame.display.update()
        
    #create the grid now that we have all of our data
    simulation_grid = Grid(pygame, game_window, HUD_scale)
    simulation_grid.simulation_setup(prey_distribtion,environment_complexity)

    
    #start the countdown before the simulation
    while count_down > 0:
        #wait
        pygame.time.delay(delay)
        
        #count the wait time
        time = time + delay
        if time > 1000: #if its 1000ms
            count_down = count_down - 1 #reduce count
            time = 0 #resent counter
        #create the text of count down
        count_down_text = bigfont.render('START IN... ' + str(count_down) + " second(s)", True, color_black)
        #background
        pygame.draw.rect(game_window, simulation_background_color, (0, 0, game_window_width, game_window_height) )
        #put it on the screen
        game_window.blit(count_down_text, (game_window_width/2, game_window_height/2))
        #check for user exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                selected = True
                count_down = -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                count_down = count_down - 1
        #draw
        pygame.display.update()
    #reset timer
    time = 0
    while run:
                            
        #wait
        pygame.time.delay(delay)
        time = time + delay
        
        #reset elements in HUD
        prey_distribtion_text = font.render('Prey Distribution: ' + prey_distribtion, True, color_black)
        environment_complexity_text = font.render('Enviornment Complexity: ' + environment_complexity, True, color_black)
        HUD = [prey_distribtion_text, environment_complexity_text]        
        prey_count_text = font.render('Prey Alive: ' + str(len(simulation_grid.prey)), True, color_black)
        HUD.append(prey_count_text)
        
        obstacle_count_text = font.render('Obstacle Count: ' + str(len(simulation_grid.obstacles)), True, color_black)
        HUD.append(obstacle_count_text)
        
        #update time if simulation is still running
        if round(time/1000) <= max_time and len(simulation_grid.prey) > 0:
            time_text = font.render('Seconds: ' + str(round(time/1000)), True, color_black)
        else:
            run = False
        #attach time, same if above not ran
        HUD.append(time_text)
        
        #how many are touched
        touched_prey_text = font.render('Prey Killed: ' + str(simulation_grid.dead_prey), True, color_black)
        HUD.append(touched_prey_text)
        
        #check for program exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                selected = True
        
        #key input
        keys = pygame.key.get_pressed()
        
        if interactive:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                simulation_grid.predator.set_x_direction(Sprite.LEFT)
                #simulation_grid.predator.update()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                simulation_grid.predator.set_x_direction(Sprite.RIGHT)
                #simulation_grid.predator.update()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                simulation_grid.predator.set_y_direction(Sprite.UP)
                #simulation_grid.predator.update()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                simulation_grid.predator.set_y_direction(Sprite.DOWN)
                #simulation_grid.predator.update()
            if keys[pygame.K_0]:
                run = False
            if keys[pygame.K_ESCAPE]:
                run = False
                selected = True
        
        #update
        if round(time/1000) < 60 and len(simulation_grid.prey) > 0:
            simulation_grid.update()
        
        #render
        pygame.draw.rect(game_window, simulation_background_color, (0, 0, game_window_width*(1-HUD_scale), game_window_height) )
        pygame.draw.rect(game_window, HUD_background_color, (game_window_width*(1-HUD_scale)+2, 0, game_window_width*HUD_scale+5, game_window_height) )
        
        #write text to the HUD sode
        for i, element in enumerate(HUD):
            game_window.blit(element, (game_window_width*(1-HUD_scale)+5,i*25+5))
        
        #render the grid
        if blind_folded and peek > 0:
            simulation_grid.render(not blind_folded)
            peek = peek - delay
        else:
            simulation_grid.render(blind_folded)
        #draw
        pygame.display.update()
    
    #here is the play again selection/end of simulation menu
    #while not selected, is bypassed if quit was pressed from anywhere above
    while not selected:
        #wait still
        pygame.time.delay(delay)
        
        #see if they pressed the X, or clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selected = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
        
        #if the width of the buttons
        if mouse_pos[0] > game_window_width*(1-HUD_scale)+20 and mouse_pos[0] < game_window_width*(1-HUD_scale)+20+200:
            
            #if the height of the play again
            if mouse_pos[1] > 300 and mouse_pos[1] < 350:
                selected = True
                play_again = True
                mouse_pos = (-1,-1)
                
            #if the height of exit
            if mouse_pos[1] > 400 and mouse_pos[1] < 450:
                selected = True
                play_again = False
                mouse_pos = (-1,-1)
                
            if mouse_pos[1] > 500 and mouse_pos[1] < 550:
                date_time = datetime.datetime.now()
                date = date_time.strftime("%m/%d/%y")
                time = date_time.strftime("%H:%M:%S %p")
                count = 0
                fn = "Results/predator_prey_simulation_" + prey_distribtion + "_" + environment_complexity + "_data.txt"
                while os.path.exists(fn):
                    count = count + 1
                    buffer = "_" + str(count)
                    fn = "Results/predator_prey_simulation_" + prey_distribtion + "_" + environment_complexity + "_data" + buffer + ".txt"
                with open(fn, "w") as file:
                    file.write("Simulation taken on " + date + " at " + time + "\n")
                    file.write("Simulation Prey Distribution: " + prey_distribtion + "\n")
                    file.write("Simulation Enviroment Complexity: " + environment_complexity + "\n")
                    file.write("Simulation Time Durration: " + str(max_time) + "\n")
                    file.write("Simulation Total Prey in Simulation: " + str(len(simulation_grid.prey)+simulation_grid.dead_prey)  + "\n")
                    file.write("Simulation Total Prey Left Alive: " + str(len(simulation_grid.prey))  + "\n")
                    file.write("Simulation Total Prey Killed: " + str(simulation_grid.dead_prey) + "\n")
                mouse_pos = (-1,-1)
                saved_to = font.render(fn, True, color_black)
        
        pygame.draw.rect(game_window, simulation_background_color, (game_window_width*(1-HUD_scale)+20, 300, 200, 50) )
        pygame.draw.rect(game_window, simulation_background_color, (game_window_width*(1-HUD_scale)+20, 400, 200, 50) )
        pygame.draw.rect(game_window, simulation_background_color, (game_window_width*(1-HUD_scale)+20, 500, 200, 50) )
        
        game_window.blit(game_over, (game_window_width*(1-HUD_scale)+5, 275))
        game_window.blit(play_again_text, (game_window_width*(1-HUD_scale)+25, 310))
        game_window.blit(play_nomore, (game_window_width*(1-HUD_scale)+25, 410))
        game_window.blit(save_to_file, (game_window_width*(1-HUD_scale)+25, 510))
        game_window.blit(saved_to, (game_window_width*(1-HUD_scale)+2, 600))
        
        #show the user what is left, since they cannot move
        simulation_grid.render(not blind_folded)
        
        #update
        pygame.display.update()
    
    #close pygame
    pygame.quit()
    #return data
    return play_again

try:
    loop = True
    while loop:
        loop = predator_prey_activity(blind_folded=True) #run the simulation
except:
    x = input("Crash") #let em know mission failed, I am not the strongest at the logging module