import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def check_power_status(url, location, search=None, provider=""):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1400,900")
    # options.add_argument("--headless=new")  # enable later if needed

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    result = {
        "found": True,
        "status": "NO CONFIRMED OUTAGE",
        "type": ""
    }

    try:
        driver.get(url)
        time.sleep(7)

        provider_l = provider.lower()

        # =====================================================
        # 🔵 ENERGEX (unchanged – working)
        # =====================================================
        if "energex" in provider_l:

            search_icon = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//i[contains(@class,'material-icons') and text()='search']"
            )))
            driver.execute_script("arguments[0].click();", search_icon)
            time.sleep(1)

            search_box = wait.until(EC.visibility_of_element_located((
                By.XPATH,
                "//input[@placeholder='Enter street, suburb or postcode']"
            )))

            search_box.clear()
            search_box.click()

            for ch in location:
                search_box.send_keys(ch)
                time.sleep(0.1)

            time.sleep(1.5)
            search_box.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            search_box.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            search_box.send_keys(Keys.ENTER)

            time.sleep(5)

            page = driver.page_source.lower()
            if any(x in page for x in [
                "planned maintenance outage",
                "unplanned outage",
                "customers affected",
                "under investigation"
            ]):
                result["status"] = "OUTAGE"
                result["type"] = "Energex confirmed"

        # =====================================================
        # 🔵 POWERCOR / CITIPOWER (unchanged – working)
        # =====================================================
        elif "powercor" in provider_l or "citipower" in provider_l:

            search_box = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//input[contains(@placeholder,'Postcode') or contains(@placeholder,'Suburb')]"
            )))
            driver.execute_script("arguments[0].click();", search_box)
            search_box.clear()

            # ⚠️ Powercor prefers full text (not slow typing)
            search_box.send_keys(location)
            time.sleep(1.2)
            #search_box.send_keys(Keys.ENTER)

            time.sleep(5)

            page = driver.page_source.lower()

            if any(x in page for x in [
                "town affected",
                "no known outages on citipower and powercor networks"
            ]):

                if "no known outages on citipower and powercor networks" in page:
                    result["status"] = "NO CONFIRMED OUTAGE"
                    result["type"] = "CitiPower / Powercor"

                elif "town affected" in page:
                    result["status"] = "OUTAGE"
                    result["type"] = "Town Affected"

                else:
                    result["status"] = "UNKNOWN"
                    result["type"] = "Unable to determine"


        # =====================================================
        # 🟣 UNITED ENERGY (NEW – requested update)
        # =====================================================
        elif "united energy" in provider_l:

            # 1️⃣ Click placeholder (real user click target)
            placeholder = wait.until(EC.element_to_be_clickable((
                By.ID,
                "react-select-outage-map-outage-search-placeholder"
            )))

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                placeholder
            )
            time.sleep(0.4)

            driver.execute_script("arguments[0].click();", placeholder)
            time.sleep(0.4)

            # 2️⃣ Get REAL input
            search_input = wait.until(EC.presence_of_element_located((
                By.ID,
                "react-select-outage-map-outage-search-input"
            )))

            # 3️⃣ Focus input properly
            driver.execute_script("arguments[0].focus();", search_input)
            time.sleep(0.3)

            # 4️⃣ CLEAR safely
            search_input.send_keys(Keys.CONTROL, "a")
            search_input.send_keys(Keys.DELETE)
            time.sleep(0.3)

            # 5️⃣ CLIPBOARD PASTE (this is the key)
            driver.execute_script("""
                navigator.clipboard.writeText(arguments[0]);
            """, location)

            time.sleep(0.3)

            search_input.send_keys(Keys.CONTROL, "v")
            time.sleep(1)

            # 6️⃣ Select first dropdown result
            search_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.4)
            search_input.send_keys(Keys.ENTER)

            time.sleep(5)

            page = driver.page_source.lower()

            if any(x in page for x in [
                "outage found",
                "No outage found"
            ]):

                if "no known outages on citipower and powercor networks" in page:
                    result["status"] = "NO CONFIRMED OUTAGE"
                    result["type"] = "CitiPower / Powercor"

                elif "town affected" in page:
                    result["status"] = "OUTAGE"
                    result["type"] = "Town Affected"

                else:
                    result["status"] = "UNKNOWN"
                    result["type"] = "Unable to determine"


        # =====================================================
        # 🟠 WESTERN POWER CHECK
        # =====================================================
        elif "western power" in provider_l:

            # 1️⃣ Wait for search input
            search_box = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//input[@placeholder='Enter your suburb']"
            )))

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                search_box
            )
            time.sleep(0.4)

            # 2️⃣ Click & focus
            driver.execute_script("arguments[0].click();", search_box)
            time.sleep(0.3)

            # 3️⃣ Clear safely
            search_box.send_keys(Keys.CONTROL, "a")
            search_box.send_keys(Keys.DELETE)
            time.sleep(0.3)

            # 4️⃣ TYPE suburb/address (normal typing works here)
            for ch in location:
                search_box.send_keys(ch)
                time.sleep(0.08)

            time.sleep(1)

            # 5️⃣ Dropdown select
            search_box.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            search_box.send_keys(Keys.ENTER)

            time.sleep(5)

            # 6️⃣ Detect outage text / list
            page = driver.page_source.lower()

            if any(x in page for x in [
                "currently has an outage",
                "is experiencing multiple outages",
                "has no known outages"
            ]):

                if "is experiencing multiple outages" in page:
                    result["status"] = "OUTAGES"
                    result["type"] = "Western Power is experiencing multiple outages"

                elif "currently has an outage" in page:
                    result["status"] = "OUTAGE"
                    result["type"] = "Western Power confirmed"

                elif "has no known outages" in page:
                    result["status"] = "NO CONFIRMED OUTAGE"
                    result["type"] = ""

                else:
                    result["status"] = "UNKNOWN"
                    result["type"] = "Unable to determine"


        # =====================================================
        # 🟠 AUSNET OUTAGE TRACKER
        # =====================================================
        elif "outagetracker.com.au" in url or "ausnet" in provider_l:

            # ==================================================
            # AUSNET – REACT DOWNSHIFT SEARCH (STABLE)
            # ==================================================

            search_input = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//input[starts-with(@id,'downshift-') and contains(@id,'-input')]"
            )))

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                search_input
            )
            time.sleep(0.4)

            driver.execute_script("arguments[0].click();", search_input)
            time.sleep(0.3)

            # Clear safely
            search_input.send_keys(Keys.CONTROL, "a")
            search_input.send_keys(Keys.DELETE)
            time.sleep(0.3)

            # Clipboard paste (MOST RELIABLE)
            driver.execute_script("""
                navigator.clipboard.writeText(arguments[0]);
            """, location)

            time.sleep(0.3)
            search_input.send_keys(Keys.CONTROL, "v")

            # Wait suggestions
            time.sleep(1.2)

            # Select first suggestion
            search_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)
            search_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)
            search_input.send_keys(Keys.ENTER)

            # Allow map + panel to update
            time.sleep(6)

            # ==================================================
            # 🔍 AUSNET OUTAGE DETECTION (FIXED LOGIC)
            # ==================================================

            panel_text = ""

            try:
                # Left-side results panel (this is where truth lives)
                left_panel = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'flex-col') or contains(@class,'col-start-1')]"
                )
                panel_text = left_panel.text.lower()
            except:
                panel_text = ""

            # --------------------------------------------------
            # 🔴 REAL OUTAGE (UNPLANNED ONLY)
            # --------------------------------------------------
            if "unplanned outage" in panel_text:
                result["status"] = "OUTAGE"
                result["type"] = "AusNet confirmed unplanned outage"
                return result

            # --------------------------------------------------
            # 🟡 PLANNED OUTAGE ONLY → NOT A POWER FAILURE
            # --------------------------------------------------
            if "planned outage" in panel_text and "unplanned outage" not in panel_text:
                result["status"] = "NO CONFIRMED OUTAGE"
                result["type"] = "Planned outage only"
                return result

            # --------------------------------------------------
            # ✅ CLEAR NO-OUTAGE STATES
            # --------------------------------------------------
            if any(x in panel_text for x in [
                "0 results for",
                "has no known outages",
                "we've had no reports of power outages"
            ]):
                result["status"] = "NO CONFIRMED OUTAGE"
                result["type"] = ""
                return result

            # --------------------------------------------------
            # 🟢 SAFE DEFAULT (VERY IMPORTANT)
            # --------------------------------------------------
            result["status"] = "NO CONFIRMED OUTAGE"
            result["type"] = ""
            return result

        # =====================================================
        # 🟠 JEMENA
        # =====================================================

        elif "jemena" in provider_l:

            # =====================================================

            # 🔵 JEMENA – Search + Blue Cluster Detection

            # =====================================================

            # 1️⃣ Wait for search input

            search_input = wait.until(EC.presence_of_element_located((

                By.ID,

                "address-search"

            )))

            # 2️⃣ Scroll + click input

            driver.execute_script(

                "arguments[0].scrollIntoView({block:'center'});",

                search_input

            )

            time.sleep(0.4)

            driver.execute_script("arguments[0].click();", search_input)

            time.sleep(0.4)

            # 3️⃣ Clear safely

            search_input.send_keys(Keys.CONTROL, "a")

            search_input.send_keys(Keys.DELETE)

            time.sleep(0.3)

            # 4️⃣ Paste full address (NO typing – stable)

            driver.execute_script("""

                navigator.clipboard.writeText(arguments[0]);

            """, location)

            time.sleep(0.3)

            search_input.send_keys(Keys.CONTROL, "v")

            time.sleep(1.2)

            # 5️⃣ Dropdown select (↓ ENTER)

            search_input.send_keys(Keys.ARROW_DOWN)

            time.sleep(0.4)

            search_input.send_keys(Keys.ENTER)

            # 6️⃣ Wait map to update

            time.sleep(6)

            # =====================================================

            # 🔥 BLUE NUMBER MARKER DETECTION (REAL SIGNAL)

            # =====================================================

            blue_markers = driver.execute_script("""

                const results = [];

                document.querySelectorAll("div").forEach(el => {

                    const style = window.getComputedStyle(el);

                    const txt = el.innerText?.trim();


                    if (

                        txt &&

                        /^[0-9]{1,2}$/.test(txt) &&               // number only

                        style.borderRadius === "50%" &&

                        style.backgroundColor.includes("rgb") &&

                        el.offsetWidth >= 30 &&

                        el.offsetHeight >= 30

                    ) {

                        results.push(txt);

                    }

                });

                return results;

            """)

            if blue_markers:

                result["status"] = "OUTAGE"

                result["type"] = f"Jemena confirmed ({sum(map(int, blue_markers))} active)"

            else:

                result["status"] = "NO CONFIRMED OUTAGE"

                result["type"] = ""


        # =====================================================
        # 🔵 FALLBACK (other providers)
        # =====================================================
        else:
            page = driver.page_source.lower()
            if any(x in page for x in [
                "planned outage",
                "unplanned outage",
                "unplanned outage",
                "customers affected"
            ]):
                result["status"] = "OUTAGE"
                result["type"] = "Detected"

    except Exception as e:
        print("ERROR:", e)
        result["found"] = False

    driver.quit()
    return result
