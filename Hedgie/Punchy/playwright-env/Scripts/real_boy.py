import csv
import random
import argparse
from playwright.sync_api import sync_playwright

def main():
    # -------------------------
    # 1. Parse command line arguments
    # -------------------------
    parser = argparse.ArgumentParser(description="Run pre- or post-test check-ins.")
    parser.add_argument("--test_type", choices=["pre", "post"], required=True,
                        help="Specify whether it's a pre-test or post-test.")
    parser.add_argument("--test_name", required=True,
                        help="Specify the test name (e.g., T5). Only rows with this value in the 'Test' column will be run.")
    parser.add_argument("--csv_path", default=r"C:\Users\alano\OneDrive\Documents\GitHub\cloud-nine\Hedgie\Punchy\playwright-env\Scripts\data.csv",
                        help="Path to the CSV file.")
    args = parser.parse_args()

    test_type = args.test_type     # "pre" or "post"
    test_name = args.test_name     # e.g. "T5"
    csv_path = args.csv_path

    # -------------------------
    # 2. Determine which columns to use
    # -------------------------
    if test_type == "pre":
        guid_column = "Pre-Test GUIDs"
        checkin_id_column = "Pre-Test Check-in ID"
    else:  # test_type == "post"
        guid_column = "Post-Test GUIDs"
        checkin_id_column = "Post-Test Check-in ID"

    # -------------------------
    # 3. Read all rows from CSV into memory
    #    We will write back any updated rows to the same file
    # -------------------------
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)  # Uses comma as the default delimiter
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # -------------------------
    # 4. Launch Playwright
    # -------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "X-CSRFToken": "AR8JeLdWskwqQWnenv8g4zVjgAygGcxd",  # If required
            }
        )

        # Add cookies
        context.add_cookies([
            {
                "name": "sessionid",
                "value": "eokz4ipj21k40migjlx6v33f6gygcq9e",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "csrftoken",
                "value": "AR8JeLdWskwqQWnenv8g4zVjgAygGcxd",
                "domain": "mathspace.co",
                "path": "/",
                "secure": True
            },
            {
                "name": "cf_clearance",
                "value": "5pWgUT174K0z.GzXVvjHr7fbmbt4g.WSkjwL9K3HBiY-1736297879-1.2.1.1-.VGw3jD_ierVR1xUkDP9zYm9fzVJA8AttsYN4CvSB_FFwJlAtvpVewrO31k33cAVp8W8o4iFrVJsrzQ5axdXkIn_Q0rvzKf9Rv0coZMGtaHMZePv7jS2gRYI.txxxu6_T19CtQ9gSMdPJtm2qxHiLBof1Rl4J8GPyOESWZY.OWyubhtSWl1XJ3QUyEZs0CxqqMiEQ_E2E5QFP1V4vnOCFKzQ6PwiVsgtktn2J3x04.Ly2WwnfY_fLAar8MLRtOQytpZyj4trp7DI_IVx2l3ESSC6qgeivFHXQwn1KdlDSpgSyFyBVuhvy3Vt5kKeP5D9nmtHGXLrewEHszOvcLWIOcIBw2qhOqf4jppLneSTYoOVaORp8qAawRT0fhoWc_TnCSdGRdsXl3SHpS0GkApaNw",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "has_logged_in",
                "value": "true",
                "domain": "mathspace.co",
                "path": "/",
            },
            {
                "name": "selected_class_id",
                "value": "334889",
                "domain": "mathspace.co",
                "path": "/",
            }
        ])

        page = context.new_page()

        # Example: Navigating somewhere to ensure session is active
        page.goto("https://mathspace.co/impersonate/stop")
        page.goto("https://mathspace.co/debug/skill-set-check-in/curriculum/LanternCurriculum-15")
        page.wait_for_load_state("networkidle")

        # Optional: verify if the page loaded properly
        if not page.is_visible("input[placeholder='Outcome IDs']"):
            print("Failed to load the page. Exiting.")
            browser.close()
            return

        print("Logged in and ready to process data.")

        # -------------------------
        # 5. Process each row
        #    - Only handle rows matching the user-specified test name
        #    - Use pre-/post- columns for GUIDs
        #    - Record the first question URL to the appropriate check-in ID column
        # -------------------------
        for row in rows:
            if row["Test"] != test_name:
                # Skip rows whose 'Test' column doesn't match the requested test
                continue

            outcome_guids = row.get(guid_column, "").strip()
            if not outcome_guids:
                print(f"Row ID {row['ID']} has no GUIDs in column '{guid_column}'. Skipping.")
                continue

            # Convert Percent Correct to float
            try:
                percent_correct = float(row["Percent Correct"])
            except ValueError:
                print(f"Invalid Percent Correct in row ID {row['ID']}. Skipping.")
                continue

            # Fill outcome IDs
            page.fill("input[placeholder='Outcome IDs']", outcome_guids)
            page.locator("button:has-text('Validate')").nth(0).click()
            page.wait_for_selector("button:has-text('Fetch Question Previews')")

            # Fill Student ID — adjust as needed (e.g., row["USERNAME"] if you prefer)
            student_id = row["ID"]
            page.fill("input[placeholder='Student ID']", student_id)

            # Click the second "Validate" button (for Student ID)
            page.locator("button:has-text('Validate')").nth(1).click()

            # Click "Start Check-In"
            page.click("button:has-text('Start Check-In')")
            page.wait_for_load_state("networkidle")

            # Capture the first question page URL
            first_question_url = page.url
            print(f"First question URL for row ID {row['ID']}: {first_question_url}")

            # Store that URL in the CSV row
            row[checkin_id_column] = first_question_url

            # Turn on dev mode in localStorage
            page.evaluate("""() => {
                localStorage.setItem('__lantern:devMode', 'true');
            }""")
            page.reload()
            page.wait_for_load_state("networkidle")

            # -------------------------
            # 6. Answer questions
            # -------------------------
            while True:
                # Handle "Continue" button
                try:
                    if page.is_visible("button:has-text('Continue')"):
                        print("Continue button detected. Skipping question.")
                        page.click("button:has-text('Continue')")
                        page.wait_for_load_state("networkidle")
                        continue
                except Exception as e:
                    print(f"Error handling Continue button: {e}")

                # Handle "Back to dashboard" button => break out if done
                if page.is_visible("button:has-text('Back to dashboard')"):
                    print(f"Finished check-in for student ID {student_id}")
                    page.click("button:has-text('Back to dashboard')")
                    break

                # Capture current question text
                try:
                    current_question = page.locator("div.css-4lpqgf-makeBodyComponent.e2zo9vh0").text_content()
                except Exception as e:
                    print(f"Error capturing current question: {e}")
                    continue

                # Decide correct or incorrect
                random_value = random.random()
                print(f"Random Value: {random_value}, Percent Correct: {percent_correct}")
                if random_value < percent_correct:
                    print(f"Answering Correct for student ID {student_id}")
                    locator = page.locator("button[aria-label='✓']")
                else:
                    print(f"Answering Incorrect for student ID {student_id}")
                    locator = page.locator("button[aria-label='✗']")

                try:
                    # Attempt to click
                    locator.click()

                    # Wait for the question number/text to change
                    page.wait_for_function(
                        f"""() => {{
                            const element = document.querySelector('div.css-4lpqgf-makeBodyComponent.e2zo9vh0');
                            return element && element.textContent !== '{current_question}';
                        }}""",
                        timeout=10000
                    )
                except Exception as e:
                    print(f"Error with answer button or waiting for next question: {e}")
                    continue

        # -------------------------
        # 7. After processing all rows, write updates back to CSV
        # -------------------------
        browser.close()

    # If the CSV didn’t include the check-in ID columns initially, make sure to add them.
    if checkin_id_column not in fieldnames:
        fieldnames.append(checkin_id_column)

    # Write the updated rows back to the same CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
