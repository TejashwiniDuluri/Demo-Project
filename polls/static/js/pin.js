var module = angular.module('myApp',[]);

function Main($scope,$http,$rootScope){


    $scope.fetchData = function(){
		$http({
			method:"GET",

	     	url:"/chapt_topic_ajax/"+$("#courseid").val()+"/"
     	 }).then( function(response, status) {
	     		$rootScope.chapterslist=response.data.chapterslist
	     		$rootScope.topicslist=response.data.topicslist
	     		console.log($rootScope.chapterslist)
    	});

     }
    $scope.topicData = function(){
 		
 		a = $("#chapterselected").val()
	    $scope.alltopics=$rootScope.topicslist
	    $scope.topics = $scope.alltopics[a]
    }
    $scope.courseData = function(){
		$http({
			method:"GET",

	     	url:"/course_chapter_ajax/"+$("#course").val()+"/"
     	 }).then( function(response, status) {
	     		$rootScope.chapterslist=response.data.chapterslist
	     		
    	});

     }
    $scope.projectData = function(){
		$http({
			method:"GET",

	     	url:"/course_project_ajax/"+$("#courseselected").val()+"/"
     	 }).then( function(response, status) {
     	 		alert("hi")
	     		$rootScope.projectslist=response.data.projectslist
	     		
    	});

     }
 }

 module.controller("MainCtrl",Main); 