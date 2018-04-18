
//BMR
//Women: BMR = 655 + (4.35 x weight in pounds) + (4.7 x height in inches) - (4.7 x age in years)
//Men: BMR = 66 + (6.23 x weight in pounds) + (12.7 x height in inches) - (6.8 x age in years)
// function calc_bmr(weight = 180, height = 69, age = 21, sex = 0) {




function c_bmr(weight , height , age , sex) {
	if(sex == 0){
		return 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age);
	}
	return 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age);
}
// function cals_burned(met = 1.0, bmr = 1925, minutes=60){
function c_burn(met, bmr, minutes) {
	return met * (bmr / 1440) * minutes;
}

function t_burn(met, bmr, cals){
	return cals / (met * (bmr / 1440));
}

function degToRad(deg){
	return deg * Math.PI / 180;
}
function r_dist(lat1, lng1, lat2, lng2){
	//Credit to https://www.movable-type.co.uk/scripts/latlong.html
	var R = 6371e3; // metres
	var φ1 = degToRad(lat1)
	var φ2 = degToRad(lat2)
	var Δφ = degToRad(lat2-lat1)
	var Δλ = degToRad(lng2-lng1)

	var a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
	        Math.cos(φ1) * Math.cos(φ2) *
	        Math.sin(Δλ/2) * Math.sin(Δλ/2);
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

	var d = R * c;

	return d;
}
exports.degreesToRadians = function(deg){
	return degToRad(deg)
}
//r_dist(30.3554513,-97.7346576,30.3012996,-97.7203696)
exports.real_distance = function(lat1, lng1, lat2, lng2) {
	return r_dist(lat1, lng1, lat2, lng2);
}

exports.calc_bmr = function(weight , height , age , sex) {
	return  c_bmr(weight , height , age , sex);
}
// function cals_burned(met = 1.0, bmr = 1925, minutes=60){

exports.cals_burned = function(met, bmr, minutes){
	return c_burn(met, bmr, minutes);
}
exports.to_burn = function(met, bmr, cals){
	return t_burn(met, bmr, cals);
}