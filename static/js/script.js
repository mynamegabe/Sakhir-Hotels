var isMobile = false; //initiate as false
// device detection
if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent)
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) {
    isMobile = true;
}

function delay (link) {
    setTimeout( function() { window.location = link }, 500 );
}

$(document).ready(function(){
  try {
    var element = document.getElementById("chatbox");
    element.scrollTop = element.scrollHeight;
  } catch(err) {
    /*none*/
  }
  var link = String(window.location);
  if (link.includes("?")) {
    var queries = link.split("?");
    queries.splice(0,1);
    if (queries[0].includes("dark=true")){
      if (link.lastIndexOf("/") == link.substring(0,link.indexOf('?')).length-1) {
        console.log("hmm" + link.lastIndexOf("/") == link.substring(0,link.indexOf('?')).length-1)
        mainpagedarkmode()
      } else {
        console.log("nah" + link.lastIndexOf("/") == link.substring(0,link.indexOf('?')).length-1)
        instantdarkmode()
      }
    }
  }

  /*Create responsiveness*/

  if (window.innerWidth * 1.5 < window.innerHeight) {
    try {
      var lefts = document.querySelectorAll('.productleft');
      lefts.forEach(left => {
        left.style.display="block";
        left.style.width="80vw";
        left.style.position="static";
        left.style.transform="none";
        left.style.margin="0 auto";
      });

      var rights = document.querySelectorAll('.productright');
      rights.forEach(right => {
        right.style.display="block";
        right.style.width="80vw";
        right.style.position="static";
        right.style.transform="none";
        right.style.margin="0 auto";
      });

      var ptexts = document.querySelectorAll('.producttext');
      ptexts.forEach(ptext => {
        ptext.style.fontSize="10px";
      });

    } catch(err) {

    }
  }

  if (window.innerWidth < window.innerHeight) {
    try {
      document.getElementById('navbar').style.display="none";
      document.getElementById('resnavbar').style.display="block";
    } catch(err) {
    document.getElementById('prodnavbar').style.display="none";
    document.getElementById('resnavbar').style.display="block";
    }
  }


  $(".havegrad").hover(function(){
    $(this)[0].classList.add('gradienttext');
  }, function() {
    try {
      $(this)[0].classList.remove('gradienttext');
    } catch(err) {
      var grad = "none";
    }
  });

  var prodmenuheight = String(document.querySelector('#productsmenu > #mainprod > ul').childElementCount * 45) + "px";

  $("#products").hover(function(){
    $(this).css("border-bottom", "2px solid red");
    $("#productsmenu").css("height", prodmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $(this).css("border-bottom", "0px solid red");
    $("#productsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
    //$("#navbarlist li").css("color", "#464446");
  });

  $("#productsmenu").hover(function(){
    $("#products").css("border-bottom", "2px solid red");
    $("#productsmenu").css("height", prodmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $("#products").css("border-bottom", "0px solid red");
    $("#productsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
    //$("#navbarlist li").css("color", "#464446");
  });

  /*var indmenuheight = String(document.querySelector('#roomsmenu > #mainprod > ul').childElementCount * 45) + "px";

  $("#rooms").hover(function(){
    $(this).css("border-bottom", "2px solid red");
    $("#roomsmenu").css("height", indmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $(this).css("border-bottom", "0px solid red");
    $("#roomsmenu").css("height", "0px");
    $("#navbar").css("background-color", "rgba(255,255,255,0)");
  });

  $("#roomsmenu").hover(function(){
    $("#rooms").css("border-bottom", "2px solid red");
    $("#roomsmenu").css("height", indmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $("#rooms").css("border-bottom", "0px solid red");
    $("#roomsmenu").css("height", "0px");
    $("#navbar").css("background-color", "rgba(255,255,255,0)");
  });
*/

  var solmenuheight = String(document.querySelector('#promotionsmenu > #mainprod > ul').childElementCount * 45) + "px";

  $("#promotions").hover(function(){
    $(this).css("border-bottom", "2px solid red");
    $("#promotionsmenu").css("height", solmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $(this).css("border-bottom", "0px solid red");
    $("#promotionsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
  });

  $("#promotionsmenu").hover(function(){
    $("#promotions").css("border-bottom", "2px solid red");
    $("#promotionsmenu").css("height", solmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $("#promotions").css("border-bottom", "0px solid red");
    $("#promotionsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
  });

  var resmenuheight = String(document.querySelector('#newsmenu > #mainprod > ul').childElementCount * 45) + "px";

  $("#news").hover(function(){
    $(this).css("border-bottom", "2px solid red");
    $("#newsmenu").css("height", resmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $(this).css("border-bottom", "0px solid red");
    $("#newsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
  });

  $("#newsmenu").hover(function(){
    $("#news").css("border-bottom", "2px solid red");
    $("#newsmenu").css("height", resmenuheight);
    $("#navbar").css("background-color", "white");
    }, function(){
    $("#news").css("border-bottom", "0px solid red");
    $("#newsmenu").css("height", "0px");
    $("#navbar").css("background-color", "white");
  });
/*------------Studio----------------*/
  $("#studiobutton").hover(function(){
    $("#studiosub").css("width","300px");
    $("#studiobutton").css("border-right","2px solid red");
  }, function() {
    $("#studiobutton").css("border-right","0px solid red");
    $("#studiosub").css("width","0px");
  });

  $("#studiosub").hover(function(){
    $("#studiobutton").css("border-right","2px solid red");
    $("#studiosub").css("width","300px");
  },function(){
    $("#studiobutton").css("border-right","0px solid red");
    $("#studiosub").css("width","0px");
  })
/*------------Studio----------------*/

/*------------Regular----------------*/
  $("#regularbutton").hover(function(){
    $("#regularsub").css("width","300px");
    $("#regularbutton").css("border-right","2px solid red");
  }, function() {
    $("#regularbutton").css("border-right","0px solid red");
    $("#regularsub").css("width","0px");
  });

  $("#regularsub").hover(function(){
    $("#regularbutton").css("border-right","2px solid red");
    $("#regularsub").css("width","300px");
  },function(){
    $("#regularbutton").css("border-right","0px solid red");
    $("#regularsub").css("width","0px");
  })
/*------------Regular----------------*/

/*------------Suites----------------*/
  $("#suitesbutton").hover(function(){
    $("#suitessub").css("width","300px");
    $("#suitesbutton").css("border-right","2px solid red");
  }, function() {
    $("#suitesbutton").css("border-right","0px solid red");
    $("#suitessub").css("width","0px");
  });

  $("#suitessub").hover(function(){
    $("#suitesbutton").css("border-right","2px solid red");
    $("#suitessub").css("width","300px");
  },function(){
    $("#suitesbutton").css("border-right","0px solid red");
    $("#suitessub").css("width","0px");
  })
/*------------Suites----------------*/

  $("#home").hover(function(){
    $(this).css("border-bottom", "2px solid red");
    $("#navbar").css("background-color", "white");
    }, function(){
    $(this).css("border-bottom", "0px solid red");
    $("#navbar").css("background-color", "white");
  });

});

$("#roomcat1").hover(function(){
  $(".catarrow1").css("opacity","1");
  console.log("oof");
  }, function(){
    $(".catarrow1").css("opacity","0");
    console.log("oof2");
});
    $(".roomcat1").css("border-bottom", "2px solid red");

$("#roomcat2").hover(function(){
  $(".catarrow2").css("opacity","1");
  }, function(){
    $(".catarrow2").css("opacity","0");
});
$("#roomcat3").hover(function(){
  $(".catarrow3").css("opacity","1");
  }, function(){
    $(".catarrow3").css("opacity","0");
});

function resopennav() {
  document.getElementById("resnavpulldown").style.maxHeight = "100vh";
  document.getElementById("navburger").setAttribute('onclick','resclosenav()')
}

function resclosenav() {
  document.getElementById("resnavpulldown").style.maxHeight="0";
  document.getElementById("navburger").setAttribute('onclick','resopennav()')
}

function scrollpage(){
  window.scrollTo(0,document.body.scrollHeight);
}

var resproddown = false;
var resinddown = false;
var resresdown = false;
var ressoldown = false;
function productsdropdown(obj) {
  if (resproddown == false) {
    obj.childNodes[0].childNodes[1].style.transform="rotate(180deg)";
    var resproductmenuheight = String(document.querySelector('#resproductmenu').childElementCount * 35) + "px";
    document.getElementById("resproductmenu").style.height=resproductmenuheight;
    resproddown = true;
  } else {
    obj.childNodes[0].childNodes[1].style.transform="rotate(0deg)";
    document.getElementById("resproductmenu").style.height="0px";
    resproddown = false;
  }
}

function roomsdropdown(obj) {
  if (resinddown == false) {
    obj.childNodes[0].childNodes[1].style.transform="rotate(180deg)";
    var resroomsmenuheight = String(document.querySelector('#resroommenu').childElementCount * 35) + "px";
    document.getElementById("resroommenu").style.height=resroomsmenuheight;
    resinddown = true;
  } else {
    obj.childNodes[0].childNodes[1].style.transform="rotate(0deg)";
    document.getElementById("resroommenu").style.height="0px";
    resinddown= false;
  }
}

function newsdropdown(obj) {
  if (resresdown == false) {
    obj.childNodes[0].childNodes[1].style.transform="rotate(180deg)";
    var resnewsmenuheight = String(document.querySelector('#resnewsmenu').childElementCount * 35) + "px";
    document.getElementById("resnewsmenu").style.height=resnewsmenuheight;
    resresdown = true;
  } else {
    obj.childNodes[0].childNodes[1].style.transform="rotate(0deg)";
    document.getElementById("resnewsmenu").style.height="0px";
    resresdown = false;
  }
}

function promotionsdropdown(obj) {
  if (ressoldown== false) {
    obj.childNodes[0].childNodes[1].style.transform="rotate(180deg)";
    var respromotionmenuheight = String(document.querySelector('#respromotionmenu').childElementCount * 35) + "px";
    document.getElementById("respromotionmenu").style.height=respromotionmenuheight;
    ressoldown = true;
  } else {
    obj.childNodes[0].childNodes[1].style.transform="rotate(0deg)";
    document.getElementById("respromotionmenu").style.height="0px";
    ressoldown = false;
  }
}


function openmenu() {
  document.getElementById("footermenu").style.height="100%";
  setTimeout(function(){window.scrollBy(0,200+window.innerHeight/2);},500);
  document.getElementById("hamburger").setAttribute("onclick","closemenu()");
  document.getElementById("hamburger").style.transform="rotate(90deg)";
}

function closemenu() {
  var scrollup = parseInt(getComputedStyle(document.getElementById("footermenu")).height);
  window.scrollBy(0,-scrollup);
  document.getElementById("hamburger").setAttribute("onclick","openmenu()");
  document.getElementById("footermenu").style.height="0px";
  document.getElementById("hamburger").style.transform="rotate(0deg)";
}

function rotatelogo() {
  document.getElementById("footerlogo").style.transform="rotate(0deg)";
  document.getElementById("footerlogo").style.transition="none";
  setTimeout(function(){
    document.getElementById("footerlogo").style.transform="rotate(360deg)";
    document.getElementById("footerlogo").style.transition="transform 0.25s";
  },250);
}


function mainpagedarkmode() {
  window.history.replaceState(null, null, "?dark=true");
  document.getElementById('darkmodeswitch').style.opacity='0';
  document.getElementById('darkmodeswitch').style.left='17px';
  document.getElementById('resdarkmodeswitch').style.opacity='0';
  document.getElementById('resdarkmodeswitch').style.left='17px';
  $("#roomform").css("filter","invert(90%)");
  document.getElementById('resnavbar').style.filter="invert(90%)";
  document.getElementById('resnavbar').style.backgroundColor="white";
  document.getElementById("resnavbar").classList.toggle('darknav');
  document.getElementById('navbar').style.filter="invert(90%)";
  document.getElementById('navbar').style.backgroundColor="white";
  document.getElementById("navbar").classList.toggle('darknav');
  $("#logo").css("filter","invert(90%)");
  setTimeout( function(){
    document.getElementById('resdarkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
    document.getElementById('resdarkmodeswitch').style.opacity='1';
    document.getElementById('resdarkmodeswitch').style.left='35px';
    document.getElementById('resdarkmodebutton').setAttribute("onclick","mainpagelightmode()");
    document.getElementById('darkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
    document.getElementById('darkmodeswitch').style.opacity='1';
    document.getElementById('darkmodeswitch').style.left='35px';
    document.getElementById('darkmodebutton').setAttribute("onclick","mainpagelightmode()");
    document.getElementById('productsmenu').style.filter="invert(90%)";
    document.getElementById('promotionsmenu').style.filter="invert(90%)";
    //document.getElementById('roomsmenu').style.filter="invert(90%)";
    document.getElementById('newsmenu').style.filter="invert(90%)";
    var changelink = String(window.location)
    if (!(changelink.includes("?dark=true"))) {
      window.location.assign(changelink.slice(0,changelink.indexOf(".html")+5)+"?dark=true")
    }

    const hyperlinks = document.querySelectorAll("a");
    hyperlinks.forEach(hyperlink => {
      var link = hyperlink.getAttribute('href');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=true";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=true" + "')";
          } else {
            var newlink = link + "?dark=true";
          }
        };
        hyperlink.setAttribute("href",newlink);
      }
    });
  },400);
  setTimeout( function(){
    document.getElementById('darkmodeswitch').style.filter="invert(90%)";
    document.getElementById('resdarkmodeswitch').style.filter="invert(90%)";
    $(".instantdelay").css("transition","filter 0.5s");
  },410);
}

function mainpagelightmode() {
  document.getElementById('darkmodeswitch').style.opacity='0';
  document.getElementById('darkmodeswitch').style.left='17px';
  document.getElementById('resdarkmodeswitch').style.opacity='0';
  document.getElementById('resdarkmodeswitch').style.left='17px';
  $("#logo").css("filter","invert(0%)");
  setTimeout( function(){
    document.getElementById('resdarkmodeswitch').setAttribute("src","/Images/Icons/sun.png");
    document.getElementById('resdarkmodeswitch').style.opacity='1';
    document.getElementById('resdarkmodeswitch').style.left='-5px';
    document.getElementById('resdarkmodebutton').setAttribute("onclick","mainpagedarkmode()");
    document.getElementById('darkmodeswitch').setAttribute("src","/Images/Icons/sun.png");
    document.getElementById('darkmodeswitch').style.opacity='1';
    document.getElementById('darkmodeswitch').style.left='-5px';
    document.getElementById('darkmodebutton').setAttribute("onclick","mainpagedarkmode()");
    document.getElementById('resnavbar').style.filter="invert(0%)";
    document.getElementById("resnavbar").classList.toggle('darknav');
    document.getElementById('navbar').style.filter="invert(0%)";
    document.getElementById("navbar").classList.toggle('darknav');
    document.getElementById('navbar').style.backgroundColor="white";
    document.getElementById('productsmenu').style.filter="invert(0%)";
    //document.getElementById('roomsmenu').style.filter="invert(0%)";
    document.getElementById('promotionsmenu').style.filter="invert(0%)";
    document.getElementById('newsmenu').style.filter="invert(0%)";
    $("#roomform").css("filter","invert(0%)");
    const hyperlinks = document.querySelectorAll("a");
    hyperlinks.forEach(hyperlink => {
      var link = hyperlink.getAttribute('href');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=false";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=false" + "')";
          } else {
            var newlink = link + "?dark=false";
          }
        }
        hyperlink.setAttribute("href",newlink);
      }
    });
  },400);
  setTimeout( function(){
    document.getElementById('darkmodeswitch').style.filter="invert(0%)";
    document.getElementById('resdarkmodeswitch').style.filter="invert(0%)";
    window.history.replaceState(null, null, "?dark=false");
  },410);
}


function darkmode() {
  window.history.replaceState(null, null, "?dark=true");
  document.getElementById('darkmodeswitch').style.opacity='0';
  document.getElementById('darkmodeswitch').style.left='17px';
  document.getElementById('resdarkmodeswitch').style.opacity='0';
  document.getElementById('resdarkmodeswitch').style.left='17px';
  setTimeout( function(){
    try {
    } catch(err) {
      //pass
    }

    var linkcheck = String(window.location)
    if (linkcheck.includes("contact")) {
      console.log("c");
      var contactimgs = document.querySelectorAll("#contactpagemenu img");
      contactimgs.forEach(contactimg => {
        contactimg.style.filter="invert(90%)";
      })
      document.querySelector("#contactpagemenu p").style.filter="invert(90%)";
      document.getElementById('contactpagenumbera').style.filter="invert(90%)";
      document.getElementById('contactpagemaila').style.filter="invert(90%)";
      document.getElementById('phoneimg').style.filter="invert(0%)";
      document.getElementById('mailimg').style.filter="invert(0%)";
    }
    document.getElementById('resdarkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
    document.getElementById('resdarkmodeswitch').style.opacity='1';
    document.getElementById('resdarkmodeswitch').style.left='35px';
    document.getElementById('resdarkmodebutton').setAttribute("onclick","lightmode()");
    document.getElementById('darkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
    document.getElementById('darkmodeswitch').style.opacity='1';
    document.getElementById('darkmodeswitch').style.left='35px';
    document.getElementById('darkmodebutton').setAttribute("onclick","lightmode()");
    document.getElementById('resnavbar').style.filter="invert(90%)";
    document.getElementById('resnavbar').style.backgroundColor="white";
    document.getElementById("resnavbar").classList.toggle('darknav');
    document.getElementById('prodnavbar').style.filter="invert(90%)";
    document.getElementById('darkmodeswitch').style.filter="invert(90%)";
    document.getElementById('productsmenu').style.filter="invert(90%)";
    //document.getElementById('roomsmenu').style.filter="invert(90%)";
    document.getElementsByTagName('BODY')[0].style.backgroundColor = "#181818";
    document.getElementById('promotionsmenu').style.filter="invert(90%)";
    document.getElementById('newsmenu').style.filter="invert(90%)";
    $(".roominfo").css("filter","invert(90%)");
    $(".roomcat").css("filter","invert(90%)");
    $("#logo").css("filter","invert(90%)");
    try {
      const paras = document.querySelectorAll('p');
      paras.forEach(para => {
        para.style.filter = "invert(90%)";
      })
      const lis = document.querySelectorAll('.producthalflist li');
      lis.forEach(li => {
        li.style.filter = "invert(90%)";
      })
    } catch(err) {
      /**/
    }
    const hOnes = document.querySelectorAll('h1');
    hOnes.forEach(hOne => {
      hOne.style.color="white"
    })
    const hTwos = document.querySelectorAll('h2');
    hTwos.forEach(hTwo => {
      hTwo.style.color="white"
    });

    const hyperlinks = document.querySelectorAll("a");
    hyperlinks.forEach(hyperlink => {
      var link = hyperlink.getAttribute('href');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=true";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=true" + "')";
          } else {
            var newlink = link + "?dark=true";
          }
        }
        hyperlink.setAttribute("href",newlink);
      } else {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=true";
        } else {
          var newlink = link + "?dark=true";
        }
        hyperlink.setAttribute("href",newlink);
      }
    });

    const divclicks = document.querySelectorAll('.roomcat')
    divclicks.forEach(divlink => {
      var link = divlink.getAttribute('onclick');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=true";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=true" + "')";
          } else {
            var newlink = link + "?dark=true";
          }
        }
        divlink.setAttribute("onclick",newlink);
      }
    });

    try {
      document.querySelectorAll("#PAarrowdown").forEach(arrow => {
        arrow.setAttribute("src","Images/Icons/arrowdown.png")
      });
    } catch (err) {
      try {
        document.querySelectorAll("#arrowdown").forEach(arrow => {
          arrow.setAttribute("src","Images/Icons/blackarrowdown.png")
        });
      } catch (err) {
        //pass
      }
    }
    console.log("Switched to dark mode");
  }, 400);
  setTimeout( function(){
    document.getElementById('darkmodeswitch').style.filter="invert(90%)";
    document.getElementById('resdarkmodeswitch').style.filter="invert(90%)";
  },410);
}


function lightmode() {
  document.getElementById('darkmodeswitch').style.opacity='0';
  document.getElementById('darkmodeswitch').style.left='17px';
  $("#logo").css("filter","invert(0%)");
  setTimeout( function(){
    try {
    } catch(err) {
      //pass
    }

    var linkcheck = String(window.location)
    if (linkcheck.includes("contact")) {
      console.log("c");
      var contactimgs = document.querySelectorAll("#contactpagemenu img");
      contactimgs.forEach(contactimg => {
        contactimg.style.filter="invert(0%)";
      });
      document.querySelector("#contactpagemenu p").style.filter="invert(0%)";
      document.getElementById('contactpagenumbera').style.filter="invert(0%)";
      document.getElementById('contactpagemaila').style.filter="invert(0%)";
    }
    document.getElementById('resdarkmodeswitch').setAttribute("src","/Images/Icons/sun.png");
    document.getElementById('resdarkmodeswitch').style.opacity='1';
    document.getElementById('resdarkmodeswitch').style.left='-5px';
    document.getElementById('resdarkmodebutton').setAttribute("onclick","darkmode()");
    document.getElementById('darkmodeswitch').setAttribute("src","/Images/Icons/sun.png");
    document.getElementById('darkmodeswitch').style.opacity='1';
    document.getElementById('darkmodeswitch').style.left='-5px';
    document.getElementById('darkmodebutton').setAttribute("onclick","darkmode()");
    document.getElementById('resnavbar').style.filter="invert(0%)";
    document.getElementById("resnavbar").classList.toggle('darknav');
    document.getElementById('prodnavbar').style.filter="invert(0%)";
    document.getElementById('darkmodeswitch').style.filter="invert(0%)";
    document.getElementById('productsmenu').style.filter="invert(0%)";
    //document.getElementById('roomsmenu').style.filter="invert(0%)";
    document.getElementById('promotionsmenu').style.filter="invert(0%)";
    document.getElementById('newsmenu').style.filter="invert(0%)";
    document.getElementsByTagName('BODY')[0].style.backgroundColor = "white";
    $(".roominfo").css("filter","invert(0%)");
    $("#roomform").css("filter","invert(0%)");
    $(".roomcat").css("filter","invert(0%)");
    try {
      const paras = document.querySelectorAll('p');
      paras.forEach(para => {
        para.style.filter = "invert(0%)";
      })
      const lis = document.querySelectorAll('.producthalflist li');
      lis.forEach(li => {
        li.style.filter = "invert(0%)";
      })
    } catch(err) {
      /**/
    }
    const hyperlinks = document.querySelectorAll("a");
    hyperlinks.forEach(hyperlink => {
      var link = hyperlink.getAttribute('href');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=false";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=false" + "')";
          } else {
            var newlink = link + "?dark=false";
          }
        }
        hyperlink.setAttribute("href",newlink);
      }
    });

    const divclicks = document.querySelectorAll('.roomcat')
    divclicks.forEach(divlink => {
      var link = divlink.getAttribute('onclick');
      if (!(link.includes("#"))) {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=false";
        } else {
          if (link.includes('delay')) {
            var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=false" + "')";
          } else {
            var newlink = link + "?dark=false";
          }
        }
        divlink.setAttribute("onclick",newlink);
      } else {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=false";
        } else {
          var newlink = link + "?dark=false";
        }
        hyperlink.setAttribute("href",newlink);
      }
    });

    const hOnes = document.querySelectorAll('h1');
    hOnes.forEach(hOne => {
      hOne.style.color="black"
    })
    const hTwos = document.querySelectorAll('h2');
    hTwos.forEach(hTwo => {
      hTwo.style.color="black"
    })

    try {
      document.querySelectorAll("#PAarrowdown").forEach(arrow => {
        arrow.setAttribute("src","Images/Icons/blackarrowdown.png")
      });
    } catch (err) {
      try {
        document.querySelectorAll("#arrowdown").forEach(arrow => {
          arrow.setAttribute("src","Images/Icons/arrowdown.png")
        });
      } catch (err) {
        //pass
      }
    }
    console.log("Switched to light mode");
  }, 400);
  setTimeout( function(){
    document.getElementById('darkmodeswitch').style.filter="invert(0%)";
    document.getElementById('resdarkmodeswitch').style.filter="invert(0%)";
    window.history.replaceState(null, null, "?dark=false");
  },410);
}

function instantdarkmode() {
  try {
  } catch(err) {
    //pass
  }

  try {
    document.getElementById("prodnavbar").style.transition="none";
  } catch(err) {
    //pass
  }

  document.getElementById("productsmenu").style.transition="height 0.5s";
  document.querySelector('body').style.transition="none";

  window.history.replaceState(null, null, "?dark=true");
  document.getElementById('darkmodeswitch').style.opacity='0';
  document.getElementById('darkmodeswitch').style.left='17px';
  try {
  } catch(err) {
    //pass
  }
  var linkcheck = String(window.location)
  if (linkcheck.includes("contact")) {
    console.log("c");
    var contactimgs = document.querySelectorAll("#contactpagemenu img");
    contactimgs.forEach(contactimg => {
      contactimg.style.filter="invert(90%)";
    });
    document.querySelector("#contactpagemenu p").style.filter="invert(90%)";
    document.getElementById('contactpagenumbera').style.filter="invert(90%)";
    document.getElementById('contactpagemaila').style.filter="invert(90%)";
    document.getElementById('phoneimg').style.filter="invert(0%)";
    document.getElementById('mailimg').style.filter="invert(0%)";
  };
  $("#logo").css("filter","invert(90%)");
  document.getElementById('resdarkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
  document.getElementById('resdarkmodeswitch').style.opacity='1';
  document.getElementById('resdarkmodeswitch').style.left='-5px';
  document.getElementById('resdarkmodebutton').setAttribute("onclick","lightmode()");
  document.getElementById('darkmodeswitch').setAttribute("src","/Images/Icons/moon.png");
  document.getElementById('darkmodeswitch').style.opacity='1';
  document.getElementById('darkmodeswitch').style.left='35px';
  document.getElementById('darkmodebutton').setAttribute("onclick","lightmode()");
  document.getElementById('resnavbar').style.filter="invert(90%)";
  document.getElementById('resnavbar').style.backgroundColor="white";
  document.getElementById("resnavbar").classList.toggle('darknav');
  document.getElementById('prodnavbar').style.filter="invert(90%)";
  document.getElementById('darkmodeswitch').style.filter="invert(90%)";
  document.getElementById('productsmenu').style.filter="invert(90%)";
  //document.getElementById('roomsmenu').style.filter="invert(90%)";
  document.getElementById('promotionsmenu').style.filter="invert(90%)";
  document.getElementById('newsmenu').style.filter="invert(90%)";
  document.getElementsByTagName('BODY')[0].style.backgroundColor = "#181818";
  $(".roominfo").css("filter","invert(90%)");
  $(".roomcat").css("filter","invert(90%)");
  try {
    const paras = document.querySelectorAll('p');
    paras.forEach(para => {
      para.style.filter = "invert(90%)";
    })
    const lis = document.querySelectorAll('.producthalflist li');
    lis.forEach(li => {
      li.style.filter = "invert(90%)";
    })
  } catch(err) {
    /**/
  }
  const hOnes = document.querySelectorAll('h1');
  hOnes.forEach(hOne => {
    hOne.style.color="white"
  })
  const hTwos = document.querySelectorAll('h2');
  hTwos.forEach(hTwo => {
    hTwo.style.color="white"
  });

  const hyperlinks = document.querySelectorAll("a");
  hyperlinks.forEach(hyperlink => {
    var link = hyperlink.getAttribute('href');
    if (!(link.includes("#"))) {
      if (link.includes("?")) {
        var indexqmark = link.indexOf("?")+1;
        link = link.slice(0,indexqmark);
        var newlink = link + "dark=true";
      } else {
        if (link.includes('delay')) {
          var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=true" + "')";
        } else {
          var newlink = link + "?dark=true";
        }
      }
      hyperlink.setAttribute("href",newlink);
    } else {
        if (link.includes("?")) {
          var indexqmark = link.indexOf("?")+1;
          link = link.slice(0,indexqmark);
          var newlink = link + "dark=true";
        } else {
          var newlink = link + "?dark=true";
        }
        hyperlink.setAttribute("href",newlink);
      }
  });

  const divclicks = document.querySelectorAll('.roomcat')
  divclicks.forEach(divlink => {
    var link = divlink.getAttribute('onclick');
    if (!(link.includes("#"))) {
      if (link.includes("?")) {
        var indexqmark = link.indexOf("?")+1;
        link = link.slice(0,indexqmark);
        var newlink = link + "dark=true";
      } else {
        if (link.includes('delay')) {
          var newlink = link.slice(0,link.indexOf(")")-1) + "?dark=true" + "')";
        } else {
          var newlink = link + "?dark=true";
        }
      }
      divlink.setAttribute("onclick",newlink);
    }
  });

  try {
    document.querySelectorAll("#PAarrowdown").forEach(arrow => {

      arrow.setAttribute("src","Images/Icons/arrowdown.png")
    });
  } catch (err) {
    try {
      document.querySelectorAll("#arrowdown").forEach(arrow => {
        arrow.setAttribute("src","Images/Icons/blackarrowdown.png")
      });
    } catch (err) {
      //pass
    }
  }
  console.log("Switched to dark mode");
  document.getElementById('darkmodeswitch').style.filter="invert(90%)";
  document.getElementById('resdarkmodeswitch').style.filter="invert(90%)";
  try {
  } catch(err) {
    //pass
  }

  setTimeout(function(){
    try {
    } catch(err) {
      //pass
    }

    try {
      document.getElementById("prodnavbar").style.transition="background-color 0.5s, filter 0.5s";
    } catch(err) {
      //pass
    }

    document.getElementById("productsmenu").style.transition="height 0.5s,filter 0.5s";
    document.querySelector('body').style.transition="background-color 0.5s";
    $(".instantdelay").css("transition","filter 0.5s");
  },500);
}

try {
  setTimeout( function() {
    const buttons = document.querySelectorAll('.animatedbtn');
    buttons.forEach(btn => {
      btn.addEventListener('click',function(e) {
        let x = "0";
        let y = "25";
        let ripples = document.createElement('span');
        ripples.style.left = x + 'px';
        ripples.style.top = y + 'px';
        this.appendChild(ripples);

        setTimeout(() => {
          ripples.remove()
        },500);
        })
      })
    }, 100)
} catch(err) {
  //
}

async function sha256(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder().encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    return hashHex;
}

function openlivechat() {
  $("#livechat").css("width","400px");
  $("#livechat").css("height","700px");
  $("#livechat").css("cursor","default");
  $("#livechatclose").css("display","block");
}

function closelivechat() {
  $("#livechat").css("width","60px");
  $("#livechat").css("height","60px");
  $("#livechat").css("cursor","pointer");
  $("#livechatclose").css("display","none");
}
