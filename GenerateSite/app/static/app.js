/**
 * Created by Matt on 1/15/18.
 */
console.log("Hello");
(function () {
    console.log('Hello2');
    var app = angular.module("GenerateManager", ['ngMaterial', 'ngMessages'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default').primaryPalette('blue').accentPalette('blue-grey')}
        );
    app.controller("myCtrl", function ($scope) {
        $scope.message = "Howdy!!";
    });
})();
//I'm a dumbass
