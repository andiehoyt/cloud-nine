import csv
import random
import argparse
import re
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
        percent_correct_column = "Pre-Test Percent Correct"
    else:  # test_type == "post"
        guid_column = "Post-Test GUIDs"
        checkin_id_column = "Post-Test Check-in ID"
        percent_correct_column = "Post-Test Percent Correct"

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
                "X-CSRFToken": "ykTwuW1T2Ztgo3zKWDCFtedBnCU5AO2G",  # If required
            }
        )

        # Add cookies
        context.add_cookies([
            {
                "name": "sessionid",
                "value": "oza8csbxdmqxdgsxg547vyrk1mlh8jq9",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "csrftoken",
                "value": "ykTwuW1T2Ztgo3zKWDCFtedBnCU5AO2G",
                "domain": "mathspace.co",
                "path": "/",
                "secure": True
            },
            {
                "name": "cf_clearance",
                "value": "1f2kke.HIb0UXGCilC6Ybbggu967K3gH9X11Qtqqves-1736361726-1.2.1.1-1QnHMSVSNpCOyamJ8Wr2v_mBWq5a9CygCQaiIewYwRvdNjt7tIigxvy4vSYYhclabN4wucvP.dXBaXtSsyNqZmu8bonxjhiU5THUoz9ngmPzTSd4TQM1SW2w8DZXLnsPECdo7UVT_QLgPck_1yYpIYsSBQ3NN8S0g9MBO_ylKTYakDmYAAcUQQQIlQZHF4HLErtTFFKubVgfeOBu_rAcGApLbsPe2CdyTqQ2WawYagrMfDzfew5OawAoL6gkZ8NxXR6w4vKUK.xIv7ggho7HAUKRHuCa5oY87RgEMohqGCXuwDQW2.g9oaJClp5fUPZj.O7VLlke8.FgyDj8EUd4llftw92p0YvXlwe7Ks0xq1VQmkCdVgg_.5ebmkHxoilALB6Vu.6YYU8cTp6oa348Cg",
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

        # Navigate somewhere to ensure session is active
        page.goto("https://mathspace.co/impersonate/stop")

        # Go to the debug skill-set-check-in page
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
        # -------------------------
        for row in rows:
            # Only handle rows matching the test_name
            if row["Test"] != test_name:
                continue

            # Skip if check-in ID is already filled
            existing_checkin_id = row.get(checkin_id_column, "").strip()
            if existing_checkin_id:
                print(
                    f"Row ID {row['ID']} already has a check-in ID = {existing_checkin_id}. Skipping."
                )
                continue

            outcome_guids = row.get(guid_column, "").strip()
            if not outcome_guids:
                print(f"Row ID {row['ID']} has no GUIDs in column '{guid_column}'. Skipping.")
                continue

            # Convert the dynamic percent-correct column to float
            try:
                percent_correct_str = row.get(percent_correct_column, "").strip()
                if not percent_correct_str:
                    print(
                        f"Row ID {row['ID']} has no value in column '{percent_correct_column}'. Skipping."
                    )
                    continue
                percent_correct = float(percent_correct_str)
            except ValueError:
                print(f"Invalid {percent_correct_column} for row ID {row['ID']}. Skipping.")
                continue

            # Fill outcome IDs
            page.fill("input[placeholder='Outcome IDs']", outcome_guids)
            page.locator("button:has-text('Validate')").nth(0).click()
            page.wait_for_selector("button:has-text('Fetch Question Previews')")

            # Fill Student ID
            student_id = row["ID"]
            page.fill("input[placeholder='Student ID']", student_id)

            # Click the second "Validate" button
            page.locator("button:has-text('Validate')").nth(1).click()

            # Click "Start Check-In" the first time
            page.click("button:has-text('Start check-in')")
            page.wait_for_load_state("domcontentloaded")

            # Wait for the button to reappear
            page.wait_for_selector("button:has-text('Start check-in')")

            # Click "Start Check-In" the second time
            page.click("button:has-text('Start check-in')")
            page.wait_for_load_state("networkidle")

            # Turn on dev mode in localStorage
            page.evaluate("""() => {
                localStorage.setItem('__lantern:devMode', 'true');
            }""")
            page.reload()
            page.wait_for_load_state("networkidle")

            # -------------------------------------------------------
            # 6. Answer questions, but capture the Check-in ID only
            #    AFTER the first question is answered
            # -------------------------------------------------------
            is_first_question = True

            while True:
                # Handle "Continue" button if it appears
                try:
                    if page.is_visible("button:has-text('Continue')"):
                        print("Continue button detected. Skipping question.")
                        page.click("button:has-text('Continue')")
                        page.wait_for_load_state("networkidle")
                        continue
                except Exception as e:
                    print(f"Error handling Continue button: {e}")

                # Handle "Back to dashboard" => done with this check-in
                if page.is_visible("button:has-text('Back to dashboard')"):
                    print(f"Finished check-in for student ID {student_id}")
                    page.click("button:has-text('Back to dashboard')")
                    break

                # Capture current question text
                try:
                    current_question = page.locator(
                        "div.css-4lpqgf-makeBodyComponent.e2zo9vh0"
                    ).text_content()
                except Exception as e:
                    print(f"Error capturing current question: {e}")
                    continue

                # Decide correct or incorrect
                random_value = random.random()
                if random_value < percent_correct:
                    print(f"Answering Correct for student ID {student_id}")
                    locator = page.locator("button[aria-label='✓']")
                else:
                    print(f"Answering Incorrect for student ID {student_id}")
                    locator = page.locator("button[aria-label='✗']")

                try:
                    locator.click()
                    # Wait for the question to change
                    page.wait_for_function(
                        f"""
                        () => {{
                            const el = document.querySelector('div.css-4lpqgf-makeBodyComponent.e2zo9vh0');
                            return el && el.textContent !== {repr(current_question)};
                        }}
                        """,
                        timeout=3000
                    )
                except Exception as e:
                    print(f"Error answering question or waiting for next question: {e}")
                    continue

                # ------------------------------------
                # If this is the FIRST question answered,
                # capture the new URL that should have LanternCheckIn-XXXX
                # ------------------------------------
                if is_first_question:
                    current_url = page.url
                    match = re.search(r'LanternCheckIn-(\d+)', current_url)
                    if match:
                        checkin_id = match.group(1)
                        row[checkin_id_column] = checkin_id
                        print(f"Recorded check-in ID for row {student_id}: {checkin_id}")

                        # ------------------------------------------------
                        # WRITE the CSV immediately so we don't lose data
                        # ------------------------------------------------
                        with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
                            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(rows)

                    else:
                        row[checkin_id_column] = ""
                        print(f"Could not find LanternCheckIn- number in URL: {current_url}")

                        # If you want to save an empty string as well:
                        with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
                            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(rows)

                    is_first_question = False

            # Navigate back to the debug page for the next row
            page.goto("https://mathspace.co/impersonate/stop")
            page.goto("https://mathspace.co/debug/skill-set-check-in/curriculum/LanternCurriculum-15")
            page.wait_for_load_state("networkidle")

        # -------------------------
        # 7. After processing all rows, optionally close the browser
        # -------------------------
        browser.close()


if __name__ == "__main__":
    main()