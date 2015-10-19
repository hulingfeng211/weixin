/**
 * Created by george on 15-7-27.
 */
console.log('runing app.js');
var newapp=angular.module('newapp',['ui.bootstrap','ngRoute','controllers']);

newapp.config(['$routeProvider','$locationProvider',function($routeProvider,$locationProvider){

    $routeProvider.when('/',{
        templateUrl:'/tpl/balance.html',
        controller:'BalanceController'
    }).when('/sendsms',{
        templateUrl:'/tpl/sendsms.html',
        controller:'SendMessageController'
    }).otherwise({
        redirectTo:'/'
    });
}]);