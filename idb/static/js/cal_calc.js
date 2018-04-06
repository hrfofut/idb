
//BMR
//Women: BMR = 655 + (4.35 x weight in pounds) + (4.7 x height in inches) - (4.7 x age in years)
//Men: BMR = 66 + (6.23 x weight in pounds) + (12.7 x height in inches) - (6.8 x age in years)
function calc_bmr(weight = 180, height = 69, age = 21, sex = 0) {
	if(sex == 0)
		return 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age);
	return 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age);
}
function cals_burned(met = 1.0, bmr = 1925, minutes=60){
	return met * (bmr / 1440) * minutes;
}
function to_burn(met, bmr, cals){
	return cals / cals_burned(met, bmr, 1);
}