
import pygame
import sys
import random
import tkinter as tk
from tkinter import filedialog



# Use tkinter to select file for baby names
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select Baby Names File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
if not file_path:
    print("No file selected. Exiting.")
    sys.exit()
with open(file_path, "r", encoding="utf-8") as f:
    names = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            name = line.split(':', 1)[0].strip()
            if name:
                names.append(name)
        else:
            names.append(line)
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
show_save_button = False
save_button_rect = None
save_message = ""

def draw_name(name):
    screen.fill((30, 30, 30))
    # Show name in center
    text = font.render(name, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text, text_rect)
    # Draw 1-10 buttons
    button_width = 50
    button_height = 50
    gap = 10
    total_width = 10 * button_width + 9 * gap
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT - 100
    global button_rects
    button_rects = []
    for i in range(10):
        rect = pygame.Rect(start_x + i * (button_width + gap), y, button_width, button_height)
        pygame.draw.rect(screen, (70, 70, 200), rect)
        num_text = small_font.render(str(i+1), True, (255, 255, 255))
        num_rect = num_text.get_rect(center=rect.center)
        screen.blit(num_text, num_rect)
        button_rects.append(rect)
    # Show instructions at bottom
    instr = small_font.render('Click a number to rank this name (1=worst, 10=best)', True, (180, 180, 180))
    instr_rect = instr.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(instr, instr_rect)
    # Show progress in top left
    seen = current_index + 1
    remaining = len(names) - seen
    progress = small_font.render(f'Seen: {seen}  Remaining: {remaining}', True, (200, 200, 200))
    screen.blit(progress, (10, 10))



def draw_summary():
    screen.fill((30, 30, 30))
    title = font.render('Summary', True, (0, 255, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)
    # Scrollable area
    visible_height = HEIGHT - 120 - 20
    line_height = 35
    lines = list(results.items())
    total_lines = len(lines)
    max_offset = max(0, total_lines * line_height - visible_height)
    global summary_scroll_offset, show_save_button, save_button_rect, save_message
    y_start = 120 - summary_scroll_offset
    for i, (name, rank) in enumerate(lines):
        y = y_start + i * line_height
        if 120 - line_height <= y < HEIGHT - 20:
            color = (0, 200, 0) if isinstance(rank, int) and rank >= 7 else (200, 200, 0) if isinstance(rank, int) else (200, 0, 0)
            line = small_font.render(f'{name}: {rank}', True, color)
            screen.blit(line, (WIDTH // 2 - 100, y))
    # Draw scroll bar if needed
    if max_offset > 0:
        bar_height = max(30, int(visible_height * visible_height / (total_lines * line_height)))
        bar_y = 120 + int((summary_scroll_offset / max_offset) * (visible_height - bar_height))
        pygame.draw.rect(screen, (100, 100, 100), (WIDTH - 20, 120, 10, visible_height))
        pygame.draw.rect(screen, (180, 180, 180), (WIDTH - 20, bar_y, 10, bar_height))
    # Draw save button
    if show_save_button:
        btn_w, btn_h = 180, 50
        btn_x = (WIDTH - btn_w) // 2
        btn_y = HEIGHT - 65
        save_button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(screen, (0, 120, 200), save_button_rect)
        btn_text = small_font.render('Save Results...', True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=save_button_rect.center)
        screen.blit(btn_text, btn_text_rect)
    if save_message:
        msg = small_font.render(save_message, True, (0, 255, 0))
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        screen.blit(msg, msg_rect)

clock = pygame.time.Clock()
button_rects = []
summary_scroll_offset = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_result:
            mouse_pos = event.pos
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(mouse_pos):
                    # Store rank (1-10)
                    results[names[current_index]] = i + 1
                    if current_index < len(names) - 1:
                        current_index += 1
                    else:
                        # All names done, sort results by rank (highest first), and show summary with save button
                        sorted_results = sorted(results.items(), key=lambda x: (isinstance(x[1], int), x[1]), reverse=True)
                        results.clear()
                        for name, rank in sorted_results:
                            results[name] = rank
                        show_save_button = True
                        save_message = ""
                        show_result = 'summary'
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and show_result == 'summary':
            mouse_pos = event.pos
            # Scroll with mouse wheel
            if event.button == 4:  # wheel up
                summary_scroll_offset = max(0, summary_scroll_offset - 35)
            elif event.button == 5:  # wheel down
                lines = list(results.items())
                visible_height = HEIGHT - 120 - 20
                line_height = 35
                total_lines = len(lines)
                max_offset = max(0, total_lines * line_height - visible_height)
                summary_scroll_offset = min(max_offset, summary_scroll_offset + 35)
            # Save button click
            if show_save_button and save_button_rect and save_button_rect.collidepoint(mouse_pos):
                root = tk.Tk()
                root.withdraw()
                save_path = filedialog.asksaveasfilename(title="Save Results As", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
                if save_path:
                    try:
                        with open(save_path, "w", encoding="utf-8") as out:
                            for name, rank in results.items():
                                out.write(f"{name}: {rank}\n")
                        save_message = f"Saved to {save_path}"
                        show_save_button = False
                    except Exception as e:
                        save_message = f"Error: {e}"
                else:
                    save_message = "Save cancelled."

        elif event.type == pygame.KEYDOWN and show_result == 'summary':
            # Scroll summary with up/down keys
            lines = list(results.items())
            visible_height = HEIGHT - 120 - 20
            line_height = 35
            total_lines = len(lines)
            max_offset = max(0, total_lines * line_height - visible_height)
            if event.key == pygame.K_UP:
                summary_scroll_offset = max(0, summary_scroll_offset - 35)
            elif event.key == pygame.K_DOWN:
                summary_scroll_offset = min(max_offset, summary_scroll_offset + 35)


    if show_result == 'summary':
        draw_summary()
    else:
        draw_name(names[current_index])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
