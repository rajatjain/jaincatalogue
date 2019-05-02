angular.module("eacPage")
	.constant("hideDescriptionCssClass", "examples-hide")
	.constant("buttonTextShowCode", "Show example code")
	.constant("buttonTextHideCode", "Hide example code")
	.controller("examplesCtrl", function($scope, hideDescriptionCssClass, buttonTextShowCode, buttonTextHideCode) {

		$scope.title = "asd";

		$scope.examples = {};
		$scope.buttonText = {};

		$scope.buttonText.mail = buttonTextShowCode;
		$scope.buttonText.article = buttonTextShowCode;
		$scope.buttonText.ddg = buttonTextShowCode;
		$scope.buttonText.links = buttonTextShowCode;
		$scope.buttonText.inter = buttonTextShowCode;
		$scope.buttonText.heroes = buttonTextShowCode;
		$scope.buttonText.ajaxPost = buttonTextShowCode;
		

		$scope.examples.mail = false;
		$scope.examples.article = false;
		$scope.examples.ddg = false;
		$scope.examples.links = false;
		$scope.examples.inter = false;
		$scope.examples.heroes = false;
		$scope.examples.ajaxPost = false;


		$scope.toggleDescription = function(example) {
			if ($scope.examples[example] !== undefined) {
				$scope.examples[example] = !$scope.examples[example];

				if ($scope.examples[example] === false) {
					$scope.buttonText[example] = buttonTextShowCode;
				} else {
					$scope.buttonText[example] = buttonTextHideCode;
				}
			}
		};

		$scope.getDescriptionClass = function(example) {

			if ($scope.examples[example] !== undefined && $scope.examples[example] === false) {
				return hideDescriptionCssClass;
			} else {
				return "";
			}

		};
	});
