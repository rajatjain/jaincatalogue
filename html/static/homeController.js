angular.module("eacPage")
.constant("buttonActiveClass", "btn-info")
.constant("inputGlowClass", "glow")
.controller("homeCtrl", function($scope, buttonActiveClass, inputGlowClass) {

	$scope.example = 1;

	$scope.changeExample = function(example) {
		$scope.example = example;
	}

	$scope.showExample = function(example) {
		return $scope.example === example;
	};

	$scope.getButtonActiveClass = function(example) {
		return $scope.example === example ? buttonActiveClass : "";
	}

	$scope.getInputGlowClass = function(example) {
		return $scope.example === example ? inputGlowClass : "";
	}

});

