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

	it('Checks that degrees to radians are being computed correctly', function(done) {
		assert.equal(calc.degreesToRadians(360), Math.PI * 2);
		done();
	});

	it('Compute distance between two co-ordinates', function(done) {
		assert.equal(Math.round(calc.real_distance(30.3554513,-97.7346576,30.3012996,-97.7203696)), 6176);
		done();
	});

	it('calculates time to burn 250 calories at MET 7.5', function(done) {
		assert.equal(Math.round(calc.to_burn(7.5, calc.calc_bmr(160, 69, 21, 0), 250)), 27);
		done();
	});
});

// calc_bmr(weight = 180, height = 69, age = 21, sex = 0) 
// function cals_burned(met = 1.0, bmr = 1925, minutes=60)
// function to_burn(met, bmr, cals)