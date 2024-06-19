import pygame
import sys
import numpy as np
pygame.init()
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (32, 32, 32)



# This fuction is used to draw the grid with the help of all the parameters , in this the color is being chosen on the basis of dead(black) or live cell(green) 
def draw_grid(screen, rows, cols,grid_s,cell_width,cell_height):
    # cell_width = WIDTH // cols
    # cell_height = HEIGHT // rows
    
    for row in range(rows):
        for col in range(cols):
            if grid_s[row][col]==1:
                color=(0,255,0)
            else:
                color=(0,0,0)    
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen,color ,rect, 2)
            pygame.draw.rect(screen, GRID_COLOR,rect, 1)
            
            
# This is the fuction responsible for the upgradation of the grid every time a new change is being done             
def update_grid(grid_s,rows,cols):
    count=0
    grid_cur=grid_s
    for i in range(rows):
        for j in range(cols):
            
            # This is the part where the main logic of the game the rules are implemeted.
            live_neghb=np.sum(grid_s[i-1:i+2,j-1:j+2])-grid_s[i,j]
            if grid_s[i,j]==1 and (live_neghb<2 or live_neghb>3):
                grid_cur[i,j]=0
                count=count +1
            elif grid_s[i,j]==0 and live_neghb==3:
                grid_cur[i,j]=1
    return grid_cur,count    
def main(rows, cols):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid")
    font = pygame.font.SysFont(None, 24)
    interactive_mode=True
    paused=True
    count_dead=0  # To count the number of cells ellapsed

    clock = pygame.time.Clock()
    running = True
    cell_width = 40     # Taking the size of the cell as uniform of 40
    cell_height = 40
    
    # The choice of the user is being asked whethere they want to manualy set the grid or want to randomly select the pattern
    choice = input("Choose initialization method (random/manual): ").strip().lower()
    if choice == 'random':
        grid_s = np.random.choice([0, 1], size=(rows, cols))
        interactive_mode=False
        initial_grid=grid_s.copy()
    elif choice == 'manual':
        grid_s =  np.zeros((rows, cols), dtype=int)
        interactive_mode=True
        initial_grid=grid_s.copy()
  
            
    else:
        print("Invalid choice. Exiting.")
        pygame.quit()
        sys.exit()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Takin the input from the mouse and on the basis of that changing the cell live or dead
            elif event.type== pygame.MOUSEBUTTONDOWN and (interactive_mode or paused or not interactive_mode):       
                x,y=pygame.mouse.get_pos()
                row=y// cell_height
                col=x// cell_width
                # grid_dead=grid_s.copy
                grid_s[row][col]=1-grid_s[row][col]
        # Taking response from the keyboard to start/ stop the game and also exiting the maual mode.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and interactive_mode:
                    interactive_mode = False
                    initial_grid=grid_s.copy()
                elif event.key == pygame.K_SPACE and not interactive_mode:
                    paused = not paused
                elif event.key == pygame.K_r: # Code to reset the pattern as it was in the starting
                    grid_s=initial_grid.copy()
                
                # To add zoom in and zoom out feature    
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Zoom in
                    cell_width=cell_width+5
                    cell_height = cell_height+5
                elif event.key == pygame.K_MINUS and  cell_width> 40:  # Zoom out
                    cell_width = cell_width-5 
                    cell_height=cell_height-5   
                            
                   
        count=0
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, rows, cols,grid_s,cell_width,cell_height)
        if not interactive_mode and not paused:
            grid_s,count=update_grid(grid_s,rows,cols)
        count_dead=count_dead+count  
        #To print the number of dead cells on the grid
        text_surface = font.render(f'Dead Cells: {count_dead}', True, (255, 255, 255)) 
        
        screen.blit(text_surface, (10, 10))    
        pygame.display.flip()
        clock.tick(5)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    WIDTH=int(input('Enter the Width of the grid'))
    HEIGHT=int(input('Enter the height of the grid'))
    rows=int(WIDTH/40)
    cols=int(HEIGHT/40)
    
    main(rows,cols)
grid_s = [[0] * cols for _ in range(rows)]
initial_grid = [[0] * cols for _ in range(rows)]

        

    
