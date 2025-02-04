import time, json
from paths import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def get_available_relics(driver: webdriver.Firefox) -> dict:
    driver.get("https://www.prydwen.gg/star-rail/guides/relic-sets")
    relic_button = driver.find_element(By.CSS_SELECTOR, "button[class='Relic Set btn btn-secondary']")
    # 3 clicks necessary, added 1 extra for safety
    relic_button.click()
    relic_button.click()
    relic_button.click()
    relic_button.click()
    relics_grid = driver.find_element(By.CSS_SELECTOR, "div[class*='relic-set-container']")
    relic_names = relics_grid.find_elements(By.XPATH, ".//h4")
    relics = []
    for relic in relic_names:
        relics.append(relic.text)

    ornament_button = driver.find_element(By.CSS_SELECTOR, "button[class='Planetary Ornament Set btn btn-secondary']")
    ornament_button.click()
    ornament_button.click()
    ornament_button.click()
    ornament_button.click()
    ornaments_grid = driver.find_element(By.CSS_SELECTOR, "div[class*='relic-set-container']")
    ornament_names = ornaments_grid.find_elements(By.XPATH, ".//h4")
    planar_ornaments = []
    for ornament in ornament_names:
        planar_ornaments.append(ornament.text)

    return {"Relics": relics, "Planar Ornaments": planar_ornaments}

def get_character_urls(driver: webdriver.Firefox) -> dict:
    driver.get("https://www.prydwen.gg/star-rail/characters")
    characters_grid = driver.find_element(By.CSS_SELECTOR, "div[class='employees-container hsr-cards']")
    character_links = characters_grid.find_elements(By.XPATH, ".//a")
    urls = {}
    for link in character_links:
        # Newly released characters have a "New" tag on their character card
        # Unreleased characters have version tag instead
        name = link.text.split("\n")
        if len(name) > 1 and name[1].casefold != "new":
            continue
        urls[name[0]] = link.get_attribute("href")
    return urls

def open_character_build_tab(driver: webdriver.Firefox):
    # Sometimes the page refreshes by itself after loading, ex: Feixiao
    # This would cause an error if find_element is run before the refresh happens
    # a few seconds sleep should fix that
    time.sleep(4)
    build_tab = driver.find_element(By.XPATH, "//div[@class='tabs']/descendant::div[5]")

    # 2 clicks usually works but on some characters you need 4
    # I put 6 clicks just in case
    build_tab.click()
    build_tab.click()
    build_tab.click()
    build_tab.click()
    build_tab.click()
    build_tab.click()

def get_relic_sets(driver: webdriver.Firefox) -> list:
    relics = []
    for i in range(1, 10, 1):
        relic_sets = driver.find_element(By.XPATH, f"(//*[contains(text(), 'Best Relic Sets')]/following-sibling::div)[{i}]")
        if relic_sets.is_displayed():
            break
    relic_set_names = relic_sets.find_elements(By.XPATH, ".//button")
    for relic in relic_set_names:
        # Text split mainly used for removing "X debuffs required" on nihility set
        relics.append(relic.text.split("\n")[0])
    relics = list(set(relics.copy()))
    print("\n")
    return relics
    
def get_planar_sets(driver: webdriver.Firefox) -> list:
    planar_ornaments = []
    for i in range(1, 10, 1):
        planar_ornament_sets = driver.find_element(By.XPATH, f"(//*[contains(text(), 'Best Planetary Sets')]/following-sibling::div)[{i}]")
        if planar_ornament_sets.is_displayed():
            break
    planar_set_names = planar_ornament_sets.find_elements(By.XPATH, ".//button")
    for ornament in planar_set_names:
        planar_ornaments.append(ornament.text)
    planar_ornaments = list(set(planar_ornaments.copy()))
    return planar_ornaments

def get_stats(driver: webdriver.Firefox) -> dict:
    stats = {}
    for i in range(1, 10, 1):
        stats_element = driver.find_element(By.XPATH, f"(//div[contains(text(), 'Best Stats')]/following-sibling::div)[{i}]")
        if stats_element.is_displayed():
            break
    stats_cols = stats_element.find_elements(By.XPATH, ".//div[@class='col']")
    for col in stats_cols:
        piece = col.find_element(By.XPATH, ".//div[@class='stats-header']/span")
        stat = []
        stat_elements = col.find_elements(By.XPATH, ".//div[@class='hsr-stat']/span")
        for i in stat_elements:
            stat.append(i.text)
        stats[piece.text] = stat
    return stats

def get_character_builds(driver: webdriver.Firefox) -> dict:
    time.sleep(1)
    build_tablist = driver.find_element(By.CSS_SELECTOR, "ul[class*='build-tab']")
    driver.execute_script('''
        arguments[0].classList.remove('single-build');
        arguments[0].classList.add('more-build'); 
    ''', build_tablist)
    build_tabs = build_tablist.find_elements(By.XPATH, ".//button")
    builds = {}
    for build in build_tabs:
        build.click()
        build.click()
        time.sleep(1)
        relics = get_relic_sets(driver)
        planar_ornaments = get_planar_sets(driver)
        stats = get_stats(driver)
        builds[build.text] = {"Relics": relics, "Planar Ornaments": planar_ornaments, "Stats": stats}
    return builds

if __name__ == "__main__":
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("browser.contentblocking.category", "strict")
    firefox_profile.set_preference("datareporting.healthreport.uploadEnabled", "false")
    firefox_profile.set_preference("privacy.fingerprintingProtection", "true")
    options.profile = firefox_profile
    driver = webdriver.Firefox(options=options)
    driver.install_addon(path=ublock_path, temporary=True)
    driver.implicitly_wait(20)

    available_relics = get_available_relics(driver)
    # available_relics = 0
    print(f"Available Relics: {available_relics}")
    print()

    urls = get_character_urls(driver)
    # urls = {"March 7th • The Hunt": "https://www.prydwen.gg/star-rail/characters/march-7th-swordmaster"}

    relic_stats = {}
    for name, url in urls.items():
        driver.get(url)
        open_character_build_tab(driver)
        builds = get_character_builds(driver)
        relic_stats[name] = builds

        print(name)
        print(f"Builds: {builds}")

    relic_data = {"Available Relics": available_relics, "Relic Stats": relic_stats}
    
    with open("Relic Data.json", "w", encoding="utf-8") as f:
        print(json.dumps(relic_data, indent=4, ensure_ascii=False), file=f)

    driver.quit()