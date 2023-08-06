# hCaptcha Solver

This is a tool for bypassing hCaptchas in Selenium.

First, create an Instance of the Captcha_Handler to load the models.

```
import captcha_handler
ch = captcha_handler.Captcha_Handler()
```

When on a website that requires a hCaptcha, simply pass the selenium webdriver object to the Captcha_Handler's solve_captcha() function.

```
from selenium import webdriver
wd = webdriver.Chrome()
# requires hCaptcha
ch.solve_captcha(wd)
```