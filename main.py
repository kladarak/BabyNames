import pygame
import sys
import random


# Read names from file
with open("Baby Names.txt", "r", encoding="utf-8") as f:
    names = [line.strip() for line in f if line.strip()]
random.shuffle(names)

# Dictionary to store results
results = {}

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Baby Name Tinder')

# Set up font
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

current_index = 0
show_result = False
result_text = ""

def draw_name(name):
    screen.fill((30, 30, 30))
    # Show name in center
    text = font.render(name, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    # Show instructions at bottom
    instr = small_font.render('Left Arrow = Reject, Right Arrow = Accept', True, (180, 180, 180))
    instr_rect = instr.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(instr, instr_rect)
    # Show progress in top left
    seen = current_index + (1 if not show_result else 0)
    remaining = len(names) - seen
    progress = small_font.render(f'Seen: {seen}  Remaining: {remaining}', True, (200, 200, 200))
    screen.blit(progress, (10, 10))

def draw_result():
    screen.fill((30, 30, 30))
    text = font.render(result_text, True, (255, 255, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_summary():
    screen.fill((30, 30, 30))
    title = font.render('Summary', True, (0, 255, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)
    y = 120
    for name, decision in results.items():
        color = (0, 200, 0) if decision == 'Accepted' else (200, 0, 0)
        line = small_font.render(f'{name}: {decision}', True, color)
        screen.blit(line, (WIDTH // 2 - 100, y))
        y += 35

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not show_result:
            if event.key == pygame.K_LEFT:
                # Swipe left (reject)
                results[names[current_index]] = 'Rejected'
                result_text = f"{names[current_index]}: Rejected"
                show_result = True
            elif event.key == pygame.K_RIGHT:
                # Swipe right (accept)
                results[names[current_index]] = 'Accepted'
                result_text = f"{names[current_index]}: Accepted"
                show_result = True
        elif event.type == pygame.KEYDOWN and show_result:
            # Any key to continue
            if current_index < len(names) - 1:
                current_index += 1
                show_result = False
            else:
                # All names done, write chosen names and show summary
                chosen = [name for name, decision in results.items() if decision == 'Accepted']
                with open("Chosen Baby Names.txt", "w", encoding="utf-8") as out:
                    for name in chosen:
                        out.write(name + "\n")
                show_result = 'summary'

    if show_result == True:
        draw_result()
    elif show_result == 'summary':
        draw_summary()
    else:
        draw_name(names[current_index])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
