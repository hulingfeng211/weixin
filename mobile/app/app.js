// 
// Here is how to define your module 
// has dependent on mobile-angular-ui
// 
var app = angular.module('app', [
  'ngRoute',
  'mobile-angular-ui',
  
  // touch/drag feature: this is from 'mobile-angular-ui.gestures.js'
  // it is at a very beginning stage, so please be careful if you like to use
  // in production. This is intended to provide a flexible, integrated and and 
  // easy to use alternative to other 3rd party libs like hammer.js, with the
  // final pourpose to integrate gestures into default ui interactions like 
  // opening sidebars, turning switches on/off ..
  'mobile-angular-ui.gestures',
    'chart.js'

]);

app.run(function($transform) {
  window.$transform = $transform;
});

// 
// You can configure ngRoute as always, but to take advantage of SharedState location
// feature (i.e. close sidebar on backbutton) you should setup 'reloadOnSearch: false' 
// in order to avoid unwanted routing.
// 
app.config(function($routeProvider,ChartJsProvider) {
  $routeProvider.when('/',              {templateUrl: 'home.html', reloadOnSearch: false});
  $routeProvider.when('/scroll',        {templateUrl: 'scroll.html', reloadOnSearch: false});
  $routeProvider.when('/toggle',        {templateUrl: 'toggle.html', reloadOnSearch: false});
  $routeProvider.when('/contactus',        {templateUrl: 'contactus.html', reloadOnSearch: false});
 /* $routeProvider.when('/tabs',          {templateUrl: 'tabs.html', reloadOnSearch: false});
  $routeProvider.when('/accordion',     {templateUrl: 'accordion.html', reloadOnSearch: false}); 
  $routeProvider.when('/overlay',       {templateUrl: 'overlay.html', reloadOnSearch: false}); 
  $routeProvider.when('/forms',         {templateUrl: 'forms.html', reloadOnSearch: false});
  $routeProvider.when('/dropdown',      {templateUrl: 'dropdown.html', reloadOnSearch: false});
  $routeProvider.when('/touch',         {templateUrl: 'touch.html', reloadOnSearch: false});
  $routeProvider.when('/swipe',         {templateUrl: 'swipe.html', reloadOnSearch: false});
  $routeProvider.when('/drag',          {templateUrl: 'drag.html', reloadOnSearch: false});
  $routeProvider.when('/drag2',         {templateUrl: 'drag2.html', reloadOnSearch: false});
  $routeProvider.when('/carousel',      {templateUrl: 'carousel.html', reloadOnSearch: false});*/

  //设置Chart的全局变量
  options={
    'colours':[
    '#f57f17', // blue
    '#ffc107', // light grey
    '#e65100', // red
    '#ff6d00', // green
    '#212121', // yellow
    '#9e9e9e', // grey
    '#4e342e'  // dark grey
  ],
    'responsive':true

  };
  ChartJsProvider.setOptions(options);
});

//
// `$touch example`
//

app.directive('toucharea', ['$touch', function($touch){
  // Runs during compile
  return {
    restrict: 'C',
    link: function($scope, elem) {
      $scope.touch = null;
      $touch.bind(elem, {
        start: function(touch) {
          $scope.touch = touch;
          $scope.$apply();
        },

        cancel: function(touch) {
          $scope.touch = touch;
          $scope.$apply();
        },

        move: function(touch) {
          $scope.touch = touch;
          $scope.$apply();
        },

        end: function(touch) {
          $scope.touch = touch;
          $scope.$apply();
        }
      });
    }
  };
}]);

//
// `$drag` example: drag to dismiss
//
app.directive('dragToDismiss', function($drag, $parse, $timeout){
  return {
    restrict: 'A',
    compile: function(elem, attrs) {
      var dismissFn = $parse(attrs.dragToDismiss);
      return function(scope, elem){
        var dismiss = false;

        $drag.bind(elem, {
          transform: $drag.TRANSLATE_RIGHT,
          move: function(drag) {
            if( drag.distanceX >= drag.rect.width / 4) {
              dismiss = true;
              elem.addClass('dismiss');
            } else {
              dismiss = false;
              elem.removeClass('dismiss');
            }
          },
          cancel: function(){
            elem.removeClass('dismiss');
          },
          end: function(drag) {
            if (dismiss) {
              elem.addClass('dismitted');
              $timeout(function() { 
                scope.$apply(function() {
                  dismissFn(scope);  
                });
              }, 300);
            } else {
              drag.reset();
            }
          }
        });
      };
    }
  };
});

//
// Another `$drag` usage example: this is how you could create 
// a touch enabled "deck of cards" carousel. See `carousel.html` for markup.
//
app.directive('carousel', function(){
  return {
    restrict: 'C',
    scope: {},
    controller: function() {
      this.itemCount = 0;
      this.activeItem = null;

      this.addItem = function(){
        var newId = this.itemCount++;
        this.activeItem = this.itemCount === 1 ? newId : this.activeItem;
        return newId;
      };

      this.next = function(){
        this.activeItem = this.activeItem || 0;
        this.activeItem = this.activeItem === this.itemCount - 1 ? 0 : this.activeItem + 1;
      };

      this.prev = function(){
        this.activeItem = this.activeItem || 0;
        this.activeItem = this.activeItem === 0 ? this.itemCount - 1 : this.activeItem - 1;
      };
    }
  };
});

app.directive('carouselItem', function($drag) {
  return {
    restrict: 'C',
    require: '^carousel',
    scope: {},
    transclude: true,
    template: '<div class="item"><div ng-transclude></div></div>',
    link: function(scope, elem, attrs, carousel) {
      scope.carousel = carousel;
      var id = carousel.addItem();
      
      var zIndex = function(){
        var res = 0;
        if (id === carousel.activeItem){
          res = 2000;
        } else if (carousel.activeItem < id) {
          res = 2000 - (id - carousel.activeItem);
        } else {
          res = 2000 - (carousel.itemCount - 1 - carousel.activeItem + id);
        }
        return res;
      };

      scope.$watch(function(){
        return carousel.activeItem;
      }, function(){
        elem[0].style.zIndex = zIndex();
      });
      
      $drag.bind(elem, {
        //
        // This is an example of custom transform function
        //
        transform: function(element, transform, touch) {
          // 
          // use translate both as basis for the new transform:
          // 
          var t = $drag.TRANSLATE_BOTH(element, transform, touch);
          
          //
          // Add rotation:
          //
          var Dx    = touch.distanceX, 
              t0    = touch.startTransform, 
              sign  = Dx < 0 ? -1 : 1,
              angle = sign * Math.min( ( Math.abs(Dx) / 700 ) * 30 , 30 );
          
          t.rotateZ = angle + (Math.round(t0.rotateZ));
          
          return t;
        },
        move: function(drag){
          if(Math.abs(drag.distanceX) >= drag.rect.width / 4) {
            elem.addClass('dismiss');  
          } else {
            elem.removeClass('dismiss');  
          }
        },
        cancel: function(){
          elem.removeClass('dismiss');
        },
        end: function(drag) {
          elem.removeClass('dismiss');
          if(Math.abs(drag.distanceX) >= drag.rect.width / 4) {
            scope.$apply(function() {
              carousel.next();
            });
          }
          drag.reset();
        }
      });
    }
  };
});

app.directive('dragMe', ['$drag', function($drag){
  return {
    controller: function($scope, $element) {
      $drag.bind($element, 
        {
          //
          // Here you can see how to limit movement 
          // to an element
          //
          transform: $drag.TRANSLATE_INSIDE($element.parent()),
          end: function(drag) {
            // go back to initial position
            drag.reset();
          }
        },
        { // release touch when movement is outside bounduaries
          sensitiveArea: $element.parent()
        }
      );
    }
  };
}]);

