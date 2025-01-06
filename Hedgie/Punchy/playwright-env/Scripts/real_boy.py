from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Add cookies and headers to the context
        context = browser.new_context(
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "X-CSRFToken": "1Xb9iH4SvDhfBU9AMYG3WRnpsvMHWNia",  # Optional if CSRF token is required in headers
            }
        )

        # Add cookies
        context.add_cookies([
            {
                "name": "sessionid",
                "value": "omg2hbl4xf87xb6ja57qx7yojb60svva",
                "domain": "mathspace.co",
                "path": "/",
                "httpOnly": True,
                "secure": True
            },
            {
                "name": "csrftoken",
                "value": "1Xb9iH4SvDhfBU9AMYG3WRnpsvMHWNia",
                "domain": "mathspace.co",
                "path": "/",
                "secure": True
            },
            {
                "name": "cf_clearance",
                "value": "BN0WNLwcsH9IZ.b3BsuKEjibyvyDrejjdSUez94wB.Y-1736199442-1.2.1.1-WfthXqao1iKVJBDEdm6tX74194UNdl0xw_oz4gZGswkvj5oh_bONsKl7xZLoWzQ1V._r5LYWDpgKQlybyy.gYF1_pJ2QNlMGnuGe.wOfWxgX5iD89.0lwCIHbO8OrDPAy4K6rTg5DesFVmhrdTjn4eG.4MMvRNX7zEx8JYPTZseHcfidVynSznLrHurhdH_h_hhDM.pxj_YQbHwA1mgIPoKRWI0J84QRLbvKGBpuUu.eZOncqt.Jcg8r3eX4e6.C1HUzEawKsXGHfPGBDv3EIcAXasT9WAP6dctffQ9kIbHSDJHUK5NA3l_tqCdauPJUuQ5jlemo6mawhRBcxjfu19Oddk9IPeVSRWXbRIfiS44Diq_HkrOb857bYypvsx2pzRef1D78HeFwbEvFGM8hBw",
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

        # Navigate to the admin dashboard or any authenticated page
        page = context.new_page()
        page.goto("https://mathspace.co/debug/skill-set-check-in/curriculum/LanternCurriculum-15")

        page.wait_for_load_state("networkidle")  # Wait until no network requests are in progress

# Verify specific elements
        try:
            # Wait for the input field and button to appear
            page.wait_for_selector("input[placeholder='Outcome IDs']", timeout=10000)  # 10 seconds
            page.wait_for_selector("button:has-text('Validate')", timeout=10000)  # Button with 'Validate'
            
            # Check if the elements are visible
            if page.is_visible("input[placeholder='Outcome IDs']") and page.is_visible("button:has-text('Validate')"):
                print("Page loaded successfully with expected elements.")
            else:
                print("Expected elements are not visible.")
        except Exception as e:
            print(f"Error during verification: {e}")
        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()
