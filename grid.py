import os

IMAGE_DIR = "characters"
README_FILE = "README.md"
IMAGES_PER_ROW = 4
IMAGE_WIDTH = 100


## eee
def make_icon_wall():
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: {IMAGE_DIR} folder not found.")
        return ""
        
    images = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith('.png')])
    if not images:
        return "No characters found."

    html_output = []
    
    for idx, filename in enumerate(images):
        name = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").title()
        
        # Build seamless zero-space tag
        tag = f'<img src="{IMAGE_DIR}/{filename}" width="{IMAGE_WIDTH}" title="{name}" alt="{name}" style="display:inline-block; margin:0; padding:0; border:0; vertical-align:middle;"/>'
        html_output.append(tag)
        
        # Break line every 4 items
        if (idx + 1) % IMAGES_PER_ROW == 0 and (idx + 1) < len(images):
            html_output.append("<br>")
            
    return "".join(html_output)

def main():
    if not os.path.exists(README_FILE):
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write("# Icons\n\n<!-- START_GRID -->\n<!-- END_GRID -->")

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = "<!-- START_GRID -->"
    end_tag = "<!-- END_GRID -->"
    
    if start_tag not in content or end_tag not in content:
        print("Missing comment tags in README!")
        return

    before_grid = content.split(start_tag)[0]
    after_grid = content.split(end_tag)[1]
    
    grid_html = make_icon_wall()
    new_readme = f"{before_grid}{start_tag}\n{grid_html}\n{end_tag}{after_grid}"
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)
        
    print("README updated successfully.")

if __name__ == "__main__":
    main()
