/**
 * Created by george on 15-7-27.
 */
var app = angular.module('controllers', []);
app.controller('BalanceController', ['$scope', '$http', function ($scope, $http) {

    $http.get("/message/balance").success(function (data, status, headers, config) {
        $scope.state_code = data['state_code'];
        $scope.message = data['message'];

    }).error(function (data, status, headers, config) {

        console.log(status);
        console.log('data:' + data);
    });
    $scope.message = "hello,world!";
}]);

app.controller('SendMessageController', ['$scope', '$http', function ($scope, $http) {


    $scope.$watch('mobile', function () {
        console.log('mobile is change');
    });

    $scope.$watch('content', function () {
        console.log('content is change');

    });
    $scope.send = function () {

        $http.post('/message/send', {
            mobile: $scope.mobile,
            content: $scope.content
        }).success(function (data, status, header, config) {

            console.log(data);

        })
    };


}]);
