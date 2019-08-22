angular.module('acl_wizard', [])

.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
})

.controller('generateProjectController', function($scope, $http) {
	$scope.projectInfo = {};

	$scope.generateProject = function () {
		$http.post('/generate', $scope.projectInfo)
			.then(function (res) {
				console.log(res);
			})
			.catch(function (error) {
				console.log(error);
			})
	}
});