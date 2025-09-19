steps = [
    "Open the homepage: https://chanakyauniversity.in/",
    "Scroll and click on 'Programs' or 'Acquire' (whichever is present).",
    "From the dropdown, click on 'Undergraduate Programmes'.",
    "On that page, click on 'School of Engineering'.",
    "Then, go to 'School of Engineering and Social Sciences'.",
    "Finally, visit the 'About Chanakya University' page."
]

print("Simulated Navigation Task for Chanakya University:\n")

for idx, step in enumerate(steps, start=1):
    input(f"{idx}. {step}\n➡Press Enter after you complete this step...")
    print("Page summary: [Enter the main heading or title you see]\n")

print(" completed.")
