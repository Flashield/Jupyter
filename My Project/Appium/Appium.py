# adb：
# adb shell dumpsys window windows | grep mFocused
# adb shell am start -W com.zxy.studentapp/.MainActivity


from appium import webdriver
import  time

desired_caps = dict()
desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '10.0'
desired_caps['platformVersion'] = '6'
desired_caps['deviceName'] = '192.168.56.101:5555'
desired_caps['appPackage'] = 'com.zxy.studentapp'
desired_caps['appActivity'] = '.MainActivity'

driver =webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(10)

driver.quit()