def bmi(weight, height):
    bmi = weight / (height ** 2)
    print('Your body mass index is: {:4.4}'.format(bmi))
    if bmi <= 15.9:
        basic_category = 'You are underweight (severe thinness)!'
    elif bmi <= 16.9:
        basic_category = 'You are underweight (moderate thinness)!'
    elif bmi <= 18.4:
        basic_category = 'You are underweight (mild thinness)!'
    elif bmi <= 24.9:
        basic_category = 'You are in normal range!'
    elif bmi <= 29.9:
        basic_category = 'You are overweight (pre-obese)!'
    elif bmi <= 34.9:
        basic_category = 'You are obese (class I)!'
    elif bmi <= 39.9:
        basic_category = 'You are obese (class I)!'
    else:
        basic_category = 'You are obese (class I)!'
    return bmi
    return basic_category
