def bmi(weight, height):
    bmi = weight / (height ** 2)
    result = 'Your body mass index is: {:4.4}'.format(bmi)
    return result

def bmi_category(weight, height):
    category = None
    bmi = weight / (height ** 2)
    if bmi <= 15.9:
        category = 'You are underweight (severe thinness)!'
    elif bmi <= 16.9:
        category = 'You are underweight (moderate thinness)!'
    elif bmi <= 18.4:
        category = 'You are underweight (mild thinness)!'
    elif bmi <= 24.9:
        category = 'You are in normal range!'
    elif bmi <= 29.9:
        category = 'You are overweight (pre-obese)!'
    elif bmi <= 34.9:
        category = 'You are obese (class I)!'
    elif bmi <= 39.9:
        category = 'You are obese (class II)!'
    else:
        category = 'You are obese (class III)!'
    return category
