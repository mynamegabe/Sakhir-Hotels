$(document).ready(function(){
  var link = String(window.location);
  if (link.includes("?")) {
    var queries = link.split("?");
    queries.splice(0,1);
    if (queries[0].includes("dark=true")){
       $("body").css("filter","invert(90%");
       $("img").css("filter","invert(90%");
       $("body").css("background-color","#1a1a1a");
    }
  }
 });