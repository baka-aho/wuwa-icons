import os

CHAR_DIR = "characters"
WEAPON_DIR = "weapons"
README_FILE = "README.md"
IMAGE_WIDTH = 100

def get_image_tags(directory):
    if not os.path.exists(directory):
        return {} if directory == WEAPON_DIR else []
        
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.png')])
    
    # Process character list directly
    if directory == CHAR_DIR:
        tags = []
        for f in files:
            name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
            tags.append(f'<img src="{directory}/{f}" width="{IMAGE_WIDTH}" title="{name}" alt="{name}" style="display:inline-block; margin:0; padding:0; border:0; vertical-align:middle;"/>')
        return "".join(tags)

    # Automatically group weapons by type keyword in file name
    categories = {"Broadblade": [], "Sword": [], "Pistol": [], "Gauntlets": [], "Rectifier": [], "Other": []}
    for f in files:
        name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
        tag = f'<img src="{directory}/{f}" width="{IMAGE_WIDTH}" title="{name}" alt="{name}" style="display:inline-block; margin:0; padding:0; border:0; vertical-align:middle;"/>'
        
        # Match type logic
        lower_name = f.lower()
        if "broad" in lower_name:
            categories["Broadblade"].append(tag)
        elif "sword" in lower_name or "blade" in lower_name:
            categories["Sword"].append(tag)
        elif "pistol" in lower_name or "gun" in lower_name:
            categories["Pistol"].append(tag)
        elif "gauntlet" in lower_name or "glove" in lower_name:
            categories["Gauntlets"].append(tag)
        elif "rectifier" in lower_name:
            categories["Rectifier"].append(tag)
        else:
            categories["Other"].append(tag)
            
    return {k: "".join(v) for k, v in categories.items() if v}

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
    
    # Generate content streams
    char_html = get_image_tags(CHAR_DIR)
    weapon_groups = get_image_tags(WEAPON_DIR)
    
    # Build complete layout string
    layout_lines = ["## Characters", "---", char_html, "\n## Weapons", "---"]
    for category_name, weapon_html in weapon_groups.items():
        layout_lines.append(f"### {category_name}\n{weapon_html}")
        
    layout = "\n".join(layout_lines)
    new_readme = f"{before_grid}{start_tag}\n{layout}\n{end_tag}{after_grid}"
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_readme)
        
    print("README layouts populated successfully.")

if __name__ == "__main__":
    main()
