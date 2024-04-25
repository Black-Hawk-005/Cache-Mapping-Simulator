import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Cache Mapping Simulator"
BACKGROUND_COLOR = (255, 255, 255)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (150, 150, 150)

# Define cache and memory parameters
L1_CACHE_SIZE = 64
VICTIM_CACHE_SIZE = 4
L2_CACHE_SIZE = 128
MAIN_MEMORY_SIZE = 128
LINE_SIZE = 4

# Initialize caches and memory with random data
L1_cache = [None] * L1_CACHE_SIZE
victim_cache = [None] * VICTIM_CACHE_SIZE
L2_cache = [None] * L2_CACHE_SIZE
main_memory = list(range(MAIN_MEMORY_SIZE))

# Function to draw caches and memory
def draw_caches_and_memory(show_main_memory):
    # Draw L1 cache
    l1_cache_rect = pygame.Rect(50, 100, 350, 500)
    pygame.draw.rect(window, BLACK, l1_cache_rect, 2)
    font = pygame.font.SysFont(None, 24)
    text = font.render("L1 Cache", True, BLACK)
    text_rect = text.get_rect(center=(l1_cache_rect.centerx, l1_cache_rect.top - 20))
    window.blit(text, text_rect)
    for i, item in enumerate(L1_cache[:L1_CACHE_SIZE // LINE_SIZE]):
        cache_item_rect = pygame.Rect(55, 105 + i * 30, 330, 30)
        pygame.draw.rect(window, WHITE if item is None else GREEN, cache_item_rect)
        if item is not None:
            text = font.render(str(item), True, BLACK)
            text_rect = text.get_rect(center=cache_item_rect.center)
            window.blit(text, text_rect)

    # Draw Victim cache
    victim_cache_rect = pygame.Rect(450, 100, 200, 150)
    pygame.draw.rect(window, BLACK, victim_cache_rect, 2)
    text = font.render("Victim Cache", True, BLACK)
    text_rect = text.get_rect(center=(victim_cache_rect.centerx, victim_cache_rect.top - 20))
    window.blit(text, text_rect)
    for i, item in enumerate(victim_cache):
        cache_item_rect = pygame.Rect(455, 105 + i * 30, 180, 30)
        pygame.draw.rect(window, WHITE if item is None else GREEN, cache_item_rect)
        if item is not None:
            text = font.render(str(item), True, BLACK)
            text_rect = text.get_rect(center=cache_item_rect.center)
            window.blit(text, text_rect)

    # Draw L2 cache
    l2_cache_rect = pygame.Rect(700, 100, 350, 500)
    pygame.draw.rect(window, BLACK, l2_cache_rect, 2)
    text = font.render("L2 Cache", True, BLACK)
    text_rect = text.get_rect(center=(l2_cache_rect.centerx, l2_cache_rect.top - 20))
    window.blit(text, text_rect)
    for i, item in enumerate(L2_cache[:L2_CACHE_SIZE // LINE_SIZE]):
        cache_item_rect = pygame.Rect(705, 105 + i * 30, 330, 30)
        pygame.draw.rect(window, WHITE if item is None else GREEN, cache_item_rect)
        if item is not None:
            text = font.render(str(item), True, BLACK)
            text_rect = text.get_rect(center=cache_item_rect.center)
            window.blit(text, text_rect)

    # Draw Main Memory if show_main_memory is True
    if show_main_memory:
        main_memory_rect = pygame.Rect(50, 650, 1100, 100)
        pygame.draw.rect(window, BLACK, main_memory_rect, 2)
        text = font.render("Main Memory", True, BLACK)
        text_rect = text.get_rect(center=(main_memory_rect.centerx, main_memory_rect.top - 20))
        window.blit(text, text_rect)

        block_width = main_memory_rect.width // 32
        block_height = main_memory_rect.height // (MAIN_MEMORY_SIZE // 32)
        for i, item in enumerate(main_memory):
            x = main_memory_rect.left + (i % 32) * block_width
            y = main_memory_rect.top + (i // 32) * block_height
            memory_item_rect = pygame.Rect(x, y, block_width, block_height)
            pygame.draw.rect(window, WHITE if item is None else GREEN, memory_item_rect)
            if item is not None:
                text = font.render(str(item), True, BLACK)
                text_rect = text.get_rect(center=memory_item_rect.center)
                window.blit(text, text_rect)

# Function to perform cache mapping using direct mapping in L1 cache
def cache_mapping(address):
    # Check L1 cache
    index = address % L1_CACHE_SIZE
    if L1_cache[index] == address:
        return "L1 Cache Hit"
    
    # Check Victim cache
    if address in victim_cache:
        return "Victim Cache Hit"
    
    # Check L2 cache
    set_index = address % (L2_CACHE_SIZE // 4)
    for i in range(4):
        if L2_cache[set_index * 4 + i] == address:
            return "L2 Cache Hit"
    
    # Replace and move the replaced value to the victim cache
    if L1_cache[index] is not None:
        # Move replaced value to the victim cache
        if None in victim_cache:
            victim_cache[victim_cache.index(None)] = L1_cache[index]
        else:
            # Move the replaced value from victim cache to L2 cache
            if None in L2_cache:
                L2_cache[L2_cache.index(None)] = victim_cache[0]
            else:
                L2_cache[0] = victim_cache[0]
            # Move replaced value from L1 cache to victim cache
            victim_cache[0] = L1_cache[index]
    # Update L1 cache with the accessed memory address
    replaced_value = L1_cache[index]
    L1_cache[index] = address
    
    return "Cache Miss"


# Function to draw the main memory button
def draw_main_memory_button():
    button_rect = pygame.Rect(WINDOW_WIDTH - 250, WINDOW_HEIGHT - 100, 200, 50)
    pygame.draw.rect(window, BUTTON_COLOR, button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Toggle Main Memory", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)
    return button_rect

# Main loop
show_main_memory = False  # Initially, do not show main memory
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if draw_main_memory_button().collidepoint(event.pos):
                show_main_memory = not show_main_memory  # Toggle the show_main_memory variable

    # Generate random memory address
    address = random.randint(0, MAIN_MEMORY_SIZE - 1)

    # Perform cache mapping
    cache_status = cache_mapping(address)

    # Draw everything
    window.fill(BACKGROUND_COLOR)
    draw_caches_and_memory(show_main_memory)
    draw_main_memory_button()

    # Display cache status
    font = pygame.font.SysFont(None, 36)
    text = font.render(cache_status, True, RED if "Miss" in cache_status else GREEN)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    window.blit(text, text_rect)

    pygame.display.update()  # Update the display
    time.sleep(0.1)  # Adjust the delay for slower simulation speed

# Quit Pygame
pygame.quit()

