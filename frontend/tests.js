"use strict";

var assert = require('assert');

var calc = require('../idb/static/js/cal_calc.js');

// Tests are hierarchical. Here we define a test suite for our calculator.
describe('Calculator Tests', function() {
	// And then we describe our testcases.
	it('calculates bmr for 160lb 21yr man', function(done) {
		assert.equal(Math.round(calc.calc_bmr(160, 69, 21, 0)), 1796);
		done();
	});

//mocha doesn't like defaults.
	// it('checks defaults', function(done) {
	// 	assert.equal(Math.round(calc.calc_bmr(180, 69, 21, 0)), Math.round(calc.calc_bmr()));
	// 	done();
	// });

	it('calculates time to burn 250 calories at MET 7.5', function(done) {
		assert.equal(Math.round(calc.to_burn(7.5, calc.calc_bmr(160, 69, 21, 0), 250)), 27);
		done();
	});
});

// calc_bmr(weight = 180, height = 69, age = 21, sex = 0) 
// function cals_burned(met = 1.0, bmr = 1925, minutes=60)
// function to_burn(met, bmr, cals)