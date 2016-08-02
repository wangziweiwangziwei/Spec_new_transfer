<%@ page language="java" contentType="text/html; charset=UTF-8"%>
 
<!DOCTYPE HTML>
<html >
<head>
	<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE9"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />

	
	<!---------------------------百度API----------------------------------------->
	<script type="text/javascript" src="http://libs.baidu.com/jquery/2.1.1/jquery.min.js"></script>
	<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=MDNPqNapg1R9y6uwgslz91aB"></script>
    
<!---------------------------百度API----------------------------------------->

<!---------------------------API-聚合---------------------------------------->
	<script type="text/javascript" src="http://api.map.baidu.com/library/TextIconOverlay/1.2/src/TextIconOverlay_min.js"></script>
	<script type="text/javascript" src="http://api.map.baidu.com/library/MarkerClusterer/1.2/src/MarkerClusterer_min.js"></script>
<!---------------------------API-聚合---------------------------------------->
	<title>map</title>
		<style type="text/css">
	
		body,html{width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}
	    #title{width: 100%; height: 5%;background-color: #ffffff;}
	    #allmap{left:5%; width: 95%;height: 95%;overflow: hidden;margin:0;font-family:"微软雅黑";position: absolute;}
	    #select1{background-color: #ffffff;}
	    #image{/*颜色对比条*/ 
			   position: fixed;
			   top:25px;
			   left:10px;
			   z-index: 100;}
	</style>
</head>
<body>
	<div id="title">
	   <form method="post">
	   <tr> <td>
	    <select id="select1" name="name1">
	         <option value="0" >----------------请选择您的电磁服务---------------
	         <option value="1" >辐射源位置及电磁功率分布态势图
	         <option value="9" >本地功率谱文件的电磁路径图
	         <option value="2" >辐射源位置及电磁功率路径分布图
	         <option value="3" >异常频点辐射源位置及等功率覆盖圆图
	         <option value="4" >登记发射台站的位置及属性显示图
	         <option value="5" >登记发射台站的当前位置及等功率覆盖圆图
	         <option value="6" >所有发射台站的位置及属性显示图
	         <option value="7" >所有注册监测终端的位置及属性显示图
	         <option value="8" >当前所有在网监测终端的位置及属性图
	    </select></td>
	    <td colspan="2">
	     <input type="button" value="确定" onclick="Query();">
	     <input id="genzong" type="button" value="跟踪" onclick="alwaysSendData();">
	     </td></tr>
	   </form>
	</div><div id="allmap"></div>
	<div id = "image"><img src="imgs/colorbar.png" ></div>
	<div id="control"> 
	</div>
</body>
<script type="text/javascript">
	//百度地图API功能
	var map = new BMap.Map("allmap");  // 创建Map实例
	map.centerAndZoom("武汉",13);       // 初始化地图,用城市名设置地图中心点
	map.enableScrollWheelZoom(true);    //开启鼠标滚轮缩放
    map.addControl(new BMap.MapTypeControl());//添加地图类型控件
	map.addControl(new BMap.ScaleControl({anchor:BMAP_ANCHOR_BOTTOM_LEFT}));//左下角添加比例尺控件
	map.addControl(new BMap.NavigationControl());//左上角添加默认地图缩放平移控件
	//marker.setAnimation(BMAP_ANIMATION_BOUNCE);//设置点的弹跳
	
	//map.addEventListener("click",function(p){alert(p.point.lng+","+p.point.lat)});
	
	//设置地图样式
	//var mapStyle={"style":"midnight"};//地图显示模板(normal,dark,light,midnight)
	//map.setMapStyle(mapStyle);
	
	//添加网格
	//var tileLayer = new BMap.TileLayer({isTransparentPng: true});
	//tileLayer.getTilesUrl = function(tileCoord, zoom) {
	//	var x = tileCoord.x;
	//	var y = tileCoord.y;
	//	return "http://developer.baidu.com/map/jsdemo/img/border.png";
	//};
	//function add_control(){
	//	map.addTileLayer(tileLayer);
	//}
	//function delete_control(){
	//	map.removeTileLayer(tileLayer);
	//}
	//add_control();

</script>
<script type="text/javascript">

    //1.splice：删除元素并添加新元素，直接对数组进行修改，返回含有被删除元素的数组。
    //arrayObject.splice(index,howmany,element1,.....,elementX)
    //index：必选，规定从何处添加/删除元素。
    //howmany：必选，规定应该删除多少元素。未规定此参数，则删除从 index 开始到原数组结尾的所有元素。
    //element1:可选，规定要添加到数组的新元素。

    var index=0;//功能码：61,62,63,64,65,66,67,68
   	var requestData = 0;      //请求
    //var responseDataArray1 = new Array();//响应数组
    //var responseDataArray2 = new Array();//响应数组
    var T1=0,T2=0;
//==========================================页面与服务器数据交互函数==========================================================//
function Query(){
	    map.clearOverlays();//清除覆蓋物
	    var obj= document.getElementById("select1");
	    var index = obj.selectedIndex; // 选中索引
	    var value= obj.options[index].value;
	    alert(value);
	    
    	switch(value){ 

    	case "0":         
    		     requestData=0;  //close the connection to database
    	         break;
    	case "1":
    		     requestData=1;
    		     break;
    	case "2":
    		     requestData=2;
    		  
		         break;
    	case "3":
    		     requestData=3;
		         break;
    	case "4":
    		     requestData=4;    		 
		         break;
    	case "5":
    		     requestData=5;
		         break;
    	case "6":
    		     requestData=6;
		         break; 
    	case "7":
    		     requestData=7;
		         break;
    	case "8":
    		     requestData=8;
    		     break;
    	case "9":
    			requestData=9;
    			break;
    	default: 
    			 alert("功能码错误！");
    		     break;
    	}
	    
    	//=============================JQuery-AJAX异步加载===================================//
    	$.post("http://localhost:8080/MapTest/QueryDataBase", 
       	        {
       				 convertData:""+(requestData)//将页面设置的地图服务参数传到服务器
                     
       			},
       		    function(responseData,status){//服务器回传的数据
       				requestData=0;//每次发完请求数据后就清除请求数据缓冲数组
       				 //window.location.reload();//刷新当前页面.
       				 alert("响应数据：\n"+responseData);

       		   if(status==="success"){//如果回传数据成功 
       	           
       		   switch(responseData.split(",")[0]){
       		   
       			case "61":
       				     var len = responseData.split("|").length;
                   var responseDataArray1 = new Array();//响应数组
                     responseDataArray1 = responseData.split("|");
                   var responseDataArray3 = new Array();
                   for(var i=0;i<len;i++){
                       var responseDataArray2 = new Array();
                     responseDataArray2.push("61");
                     responseDataArray2.push(responseDataArray1[i].split(",")[6]);// nx////
                     responseDataArray2.push(responseDataArray1[i].split(",")[7]);// ny////
                    responseDataArray2.push(responseDataArray1[i].split(",")[8]);// △////返回参数
                     responseDataArray2.push(responseDataArray1[i].split(",")[10]);// longitude////
                     responseDataArray2.push(responseDataArray1[i].split(",")[11]);// latitude////
                     responseDataArray2.push(responseDataArray1[i].split(",")[12]);// height////
                     responseDataArray2.push(responseDataArray1[i].split(",")[13]);// power////
                     responseDataArray2.push(responseDataArray1[i].split(",")[14]);// index////
                     responseDataArray3[i] = responseDataArray2;
                   };
     
       				     
       		
       				    T1 = window.setInterval(function(){ 
       					        			
       				    	 index1_go(responseDataArray3[T2]);
                     T2++;   
       					     if( T2>=len )
       						     window.clearInterval(T1); 
       					     }, (1/12.0)*1*60000);
        	             
        	             //setTimeout(function(){index1_go(responseData.split("|")[1].split(","));},3000);
        	             //setTimeout(function(){index1_go(responseData.split("|")[2].split(","));},5000);
       	    	         break;
       	    	case "62": 
       	    		
       	    		     var len = responseData.split("|").length;
                       var responseDataArray1 = new Array();//响应数组
                       var responseDataArray2 = new Array();//响应数组
                     responseDataArray1 = responseData.split("|");
              
                     for(var i=0;i<len;i++){
                         responseDataArray2.push(responseDataArray1[i].split(",")[5]);// longitude////
                         responseDataArray2.push(responseDataArray1[i].split(",")[6]);// latitude////
                         responseDataArray2.push(responseDataArray1[i].split(",")[8]);// power////
                     }
    				     
    	   
       	    		     index2_go(responseDataArray2);
                     break;
       	    	case "63":
       	    		     
       	    		      var len = responseData.split("|").length;
                     var responseDataArray1 = new Array();//响应数组
                   responseDataArray1 = responseData.split("|");
                     var responseDataArray2 = new Array();//响应数组
                   for(var i=0;i<len;i++){
                       responseDataArray2.push("63");
                       responseDataArray2.push(responseDataArray1[i].split(",")[1]);// 归属////
                       responseDataArray2.push(responseDataArray1[i].split(",")[2]);// longitude////
                       responseDataArray2.push(responseDataArray1[i].split(",")[3]);// latitude////
                       responseDataArray2.push(responseDataArray1[i].split(",")[4]);// 高////
                       responseDataArray2.push(responseDataArray1[i].split(",")[5]);// 中心频率////
                       responseDataArray2.push(responseDataArray1[i].split(",")[6]);// 带宽////
                       responseDataArray2.push(responseDataArray1[i].split(",")[7]);// 调制参数////
                       responseDataArray2.push(responseDataArray1[i].split(",")[8]);// 调制方式////
                       responseDataArray2.push(responseDataArray1[i].split(",")[9]);// 传输功率////
                       responseDataArray2.push(responseDataArray1[i].split(",")[10]);// 衰减指数////
                       responseDataArray2.push(responseDataArray1[i].split(",")[11]);// 活跃度////
                       responseDataArray2.push(responseDataArray1[i].split(",")[12]);// 业务属性////
                       responseDataArray2.push(responseDataArray1[i].split(",")[13]);// 是否非法////

                        index3_go(responseDataArray2);
                        responseDataArray2.splice(0,responseDataArray2.length);
                        }
                        break;
       	    	case "66":
       	    		
       	    	case "64":
       	    	        var len = responseData.split("|").length;
                         var responseDataArray1 = new Array();//响应数组
                       responseDataArray1 = responseData.split("|");
                         var responseDataArray2 = new Array();//响应数组
                       for(var i=0;i<len;i++){            
                           responseDataArray2.push(responseDataArray1[i].split(",")[1]);// 归属////
                           responseDataArray2.push(responseDataArray1[i].split(",")[2]);// 台站ID////
                           responseDataArray2.push(responseDataArray1[i].split(",")[3]);// 经度////
                           responseDataArray2.push(responseDataArray1[i].split(",")[4]);// 纬度////
                           responseDataArray2.push(responseDataArray1[i].split(",")[5]);// 高////
                           responseDataArray2.push(responseDataArray1[i].split(",")[6]);// 起始频率////
                           responseDataArray2.push(responseDataArray1[i].split(",")[7]);// 终止频率////
                           responseDataArray2.push(responseDataArray1[i].split(",")[8]);// 最大传输功率////
                           responseDataArray2.push(responseDataArray1[i].split(",")[9]);// 带宽////
                           responseDataArray2.push(responseDataArray1[i].split(",")[10]);// 调制方式////
                           responseDataArray2.push(responseDataArray1[i].split(",")[11]);// 调制指数////
                           responseDataArray2.push(responseDataArray1[i].split(",")[12]);// 业务属性////
                           responseDataArray2.push(responseDataArray1[i].split(",")[13]);// 覆盖半径////
                           responseDataArray2.push(responseDataArray1[i].split(",")[14]);// 活跃度////
                       
                       }
                       index4_go(responseDataArray2);
                       
                     break;
       	    	case "65":
       	    		    
                     var len = responseData.split("|").length;
                         var responseDataArray1 = new Array();//响应数组
                       responseDataArray1 = responseData.split("|");
                         var responseDataArray2 = new Array();//响应数组
                       for(var i=0;i<len;i++){
                           responseDataArray2.push("65");
                           responseDataArray2.push(responseDataArray1[i].split(",")[1]);// 归属////
                         responseDataArray2.push(responseDataArray1[i].split(",")[2]);// 台站ID////
                         responseDataArray2.push(responseDataArray1[i].split(",")[3]);// 经度////
                         responseDataArray2.push(responseDataArray1[i].split(",")[4]);// 纬度////
                         responseDataArray2.push(responseDataArray1[i].split(",")[5]);// 高////
                           responseDataArray2.push(responseDataArray1[i].split(",")[6]);// 中心频率////
                           responseDataArray2.push(responseDataArray1[i].split(",")[7]);// 传输功率////
                           responseDataArray2.push(responseDataArray1[i].split(",")[8]);// 衰减指数////
                           responseDataArray2.push(responseDataArray1[i].split(",")[9]);// 带宽////
                           responseDataArray2.push(responseDataArray1[i].split(",")[10]);// 调制方式////
                           responseDataArray2.push(responseDataArray1[i].split(",")[11]);// 调制参数////
                           responseDataArray2.push(responseDataArray1[i].split(",")[12]);// 业务属性////
                           responseDataArray2.push(responseDataArray1[i].split(",")[13]);// 活跃度////
                           responseDataArray2.push(responseDataArray1[i].split(",")[14]);// 是否非法////
                           index5_go(responseDataArray2); 
                       responseDataArray2.splice(0,responseDataArray2.length);
                       }
       			         break;
       			/*
       	    	case "66":
       	    		    responseDataArray1 = responseData.split(",");
                         index6_go(responseDataArray1);
                     //alert("将显示所有发射台站的位置及属性显示图");
                     break;
                     */
       	    	case "67":
       	    		      var len = responseData.split("|").length;
                       var responseDataArray1 = new Array();//响应数组
                     responseDataArray1 = responseData.split("|");
                       var responseDataArray2 = new Array();//响应数组
                     for(var i=0;i<len;i++){
                         responseDataArray2.push("67");
                         responseDataArray2.push(responseDataArray1[i].split(",")[1]);// 终端ID////
                           responseDataArray2.push(responseDataArray1[i].split(",")[2]);// 等级////
                           responseDataArray2.push(responseDataArray1[i].split(",")[3]);// 经度////
                           responseDataArray2.push(responseDataArray1[i].split(",")[4]);// 纬度////
                           responseDataArray2.push(responseDataArray1[i].split(",")[5]);// 高////
                         responseDataArray2.push(responseDataArray1[i].split(",")[6]);// 注册时间////
                         responseDataArray2.push(responseDataArray1[i].split(",")[7]);// 最近一次登陆时间////

                     index7_go(responseDataArray2); 
                     responseDataArray2.splice(0,responseDataArray2.length);
                     }
       			         break;
       	    	case "68":
       	    		      var len = responseData.split("|").length;
                         var responseDataArray1 = new Array();//响应数组
                       responseDataArray1 = responseData.split("|");
                         var responseDataArray2 = new Array();//响应数组
                       for(var i=0;i<len;i++){
                           responseDataArray2.push("67");
                           responseDataArray2.push(responseDataArray1[i].split(",")[1]);// 终端ID////
                             responseDataArray2.push(responseDataArray1[i].split(",")[2]);// 等级////
                             responseDataArray2.push(responseDataArray1[i].split(",")[3]);// 经度////
                             responseDataArray2.push(responseDataArray1[i].split(",")[4]);// 纬度////
                             responseDataArray2.push(responseDataArray1[i].split(",")[5]);// 高////
                           responseDataArray2.push(responseDataArray1[i].split(",")[6]);// 注册时间////
                           responseDataArray2.push(responseDataArray1[i].split(",")[7]);// 最近一次登陆时间////

                   index8_go(responseDataArray2); 
                   responseDataArray2.splice(0,responseDataArray2.length);
                   }
     			         break;
       	    	case "69":
          		     var len = responseData.split("|").length;
                     var responseDataArray1 = new Array();//响应数组
                     var responseDataArray2 = new Array();//响应数组
                   responseDataArray1 = responseData.split("|");
            
                   for(var i=0;i<len;i++){
                       responseDataArray2.push(responseDataArray1[i].split(",")[1]);// longitude////
                       responseDataArray2.push(responseDataArray1[i].split(",")[2]);// latitude////
                   }
                     index9_go(responseDataArray2);
  				     break;
       	    	  default: 
       	    			 alert("返回信息有错误！");
       	    		     break;
       		    }
       			}	 
    	
       		//requestData.splice(0,requestData.length);//每次发完请求数据后就清除请求数据缓冲数组

       		 });

        T1=0;
        T2=0;
       			//responseDataArray1.splice(0,responseDataArray.length);
       			//responseDataArray2.splice(0,responseDataArray.length);
}

/************************************************1.态势图显示函数******************************************************************/
function index1_go(array){
  
  // map.clearOverlays();
  /*
    var PI = Math.PI;
    var H0=6378137;//地球半径，单位米
    var mConstant=21600;//计算的常数：360*60
  */
    var mLngitude;//经度
    var mLatitude;//纬度
    var mHeight;//高度
    var mPower;//功率值
    var mindex;//损耗指数
    var mRadius; //半径
    var mRatio;//分辨率
    /*
    var DetaY;//南-北网格边长
    var DetaX;//东-西网格边长
    var Nx;//= (int) (mRadius/DetaX);
    var Ny;//= (int) (mRadius/DetaY);
    var dd;//距离平方
    */
    var d;//距离
 
   mLngitude=array[4]*1;
   mLatitude=array[5]*1;
   mHeight=array[6]*1;
   mPower=array[7]*1;
   mindex=array[8]*1;
   mRadius=0;
   /*
   mRatio=array[3]*1;
   Nx=array[1]*1;
   Ny=array[2]*1;
   
	var mLngitude = array[0].LONGITUDE;
	var mLatitude = array[0].LATITUDE;
	var mHeight = array[0].HEIGHT;
	var mPower = array[0].TRANSFERPOWER;
	var mindex = array[0].TRANSINDEX;
	var mRadius = 0;
	var d;//距离
	*/

	var point = new BMap.Point(mLngitude, mLatitude);
	map.centerAndZoom(point, 13);
	
	var circle;
	var p = {
		fillColor : "",
		fillOpacity : 0.6,
		//strokeColor : "",
		strokeOpacity : 0.01,
		strokeWeight : 0.01
	};
	var label;
	var colors = [ "#red", "orange","#969600","yellow","green","blue" ];
	
	for (var i = 5; i >= 0; i--) {
		
		d = Math.sqrt(Math.pow(10, 10 * i / (5 * 1.3)));//每10dbm一个圆,衰减1.3
		p.fillColor = colors[i];
	    circle = new BMap.Circle(point, d, p );
		map.addOverlay(circle);//增加圆
		
		label = new BMap.Label("功率值:" + (mPower - i * 10) + "dbm", {
			position : new BMap.Point(point.lng, point.lat + ((d) / (2 * Math.PI * 6378137)) * 360),
			offset : new BMap.Size(5, -15)
		});
		label.setStyle({
			color : "yellow",
			backgroundColor : "gray"
		});
		map.addOverlay(label);
	}
	
   
   
}

/************************************************************************************************************************/
/************************************************2.路径图显示函数************************************************************/     
function index2_go(array){
	
 
   
   map.centerAndZoom(new BMap.Point(114.420239, 30.515488), 15);

	var len = array.length/3;
	var points = [];
	var points1 = [];
	var colors = [ "#960000", "#C80006", "#E10006", "#F50400", "#FD2D00",
			"#FA5000", "#FF7302", "#FFb600", "#FFD600", "#FBFF0E",
			"#DBFE00", "#B0FF4E", "#7FFE7D", "#5EFE9F", "#35FCC8",
			"#04FDC5", "#06E6DC", "#02CEFF", "#08AAFF", "#0895FF",
			"#0376FF", "#005BFF", "#1717FF", "#0000DB", "#0000BD",
			"#0000A2", "#000082" ];
	/*********GPS坐标转换—8阶椭圆FIR低通器滤波***********/

	/**********************************************/

	var ccs = [];
	var cc;
	var m = 0;
	for (var i = 0; i < len; i++) {
		//points.push(new BMap.Point(1*array[i].LONGITUDE+0.01217, 1*array[i].LATITUDE+0.0118));//将返回的数据解析解析成点的数组
		points.push(new BMap.Point(1 * parseFloat(array[3*i]) + 0.012,1 *parseFloat( array[3*i+1]) + 0.003745));//将返回的数据解析解析成点的数组

		m = array[3*i+2];
		if (m > -40) {
			cc = '#960000';
		} else if (m > -45) {
			cc = '#E10006';
		} else if (m > -50) {
			cc = '#FA5000';
		} else if (m > -55) {
			cc = '#FBFF0E';
		} else if (m > -60) {
			cc = '#DBFE00';
		} else if (m > -65) {
			cc = '#B0FF4E';
		} else if (m > -70) {
			cc = '#7FFE7D';
		} else if (m > -75) {
			cc = '#5EFE9F';
		} else if (m > -80) {
			cc = '#35FCC8';
		} else if (m > -85) {
			cc = '#02CEFF';
		} else if (m > -90) {
			cc = '#08AAFF';
		} else if (m > -95) {
			cc = '#0376FF';
		} else if (m > -100) {
			cc = '#005BFF';
		} else if (m > -105) {
			cc = '#0000DB';
		} else
			cc = '#0000FF';
		ccs.push(cc);
	}

	var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png",
			new BMap.Size(23, 25), {
				offset : new BMap.Size(10, 25),
				imageOffset : new BMap.Size(0, 0 - 0 * 25)
			});
	map.addOverlay(new BMap.Marker(points[0], {
		icon : myIcon
	}));
 T1 = window.setInterval(function() {

		//map.centerAndZoom(points[T2],16);  
		//添加远点到地图 
		var circle = new BMap.Circle(points[T2], 20);
		circle.setFillColor(ccs[T2]);
		circle.setStrokeWeight(0.1);
		circle.setFillOpacity(0.8);
		map.addOverlay(circle);//增加圆 

	/* 	//添加折线到地图上
		var polyline = new BMap.Polyline(points, {strokeColor:"blue", strokeWeight:5, strokeOpacity:0.6});
		map.addOverlay(polyline); */
		 T2++;
		if (T2 > (len - 2))
			window.clearInterval(T1);
	}, 100); 

   
   
    
}
/************************************************************************************************************************/
/********************************************3.异常频点辐射源位置及等功率覆盖圆图显示函数*******************************************/  

function index3_go(array){
      //map.clearOverlays();
      
      var point = new BMap.Point(array[2]*1,array[3]*1);
      map.centerAndZoom(point,13);////////////

    var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png", new BMap.Size(23, 25),{offset: new BMap.Size(10, 25),imageOffset: new BMap.Size(0, 0-4*25)}); 
      var marker = new BMap.Marker(point, {icon: myIcon});
    //var label = new BMap.Label("异常频点辐射源的位置："+"经度"+point.lng+",纬度"+point.lat+"<br>"+"属性：",{offset:new BMap.Size(10,20)});
    //label.setStyle({ color : "blue" ,backgroundColor:"gray"});
    //marker.setLabel(label);
      map.addOverlay(marker);
      var content =                  
          "<br>"+"归属单位："+array[1]
       +"<br>"+"时间占用度："+array[11]
         +"<br>"+"业务属性判断结果："+array[12]
         +"<br>"+"是否合法："+array[13]
         +"<br>"+"中心频率："+array[5]
         +"<br>"+"带宽："+array[6]
         +"<br>"+"调制方式："+array[8]
         +"<br>"+"调制参数："+array[7]
         +"<br>"+"地理位置："+array[2]+","+array[3]+","+array[4]
         +"<br>"+"传输功率："+array[9]
         +"<br>"+"衰减指数："+array[10];
      addClickHandler4(content,marker);
    //marker.setAnimation(BMAP_ANIMATION_BOUNCE);
		var strokeColors = [ "#960000", "#FD2D00", "#FFb600", "#FFD600","#7FFE7D", "#02CEFF", "#aabbcc" ];
		var d = 0;
		for (var i = 0; i < strokeColors.length; i++) {

			d = Math.sqrt(Math.pow(10, 10 * i / (5 * 2)));//每10dbm一个圆

			var circle = new BMap.Circle(point, d, {
				strokeColor : strokeColors[i],
				fillColor : "",
				strokeWeight : 3,
				strokeStyle : "",
				strokeOpacity : 0.8
			});
			map.addOverlay(circle);//增加圆
			circle.addEventListener("click", function(e) {alert("功率值:" + e.target.getStrokeColor());});

			var label = new BMap.Label("功率值:" + (array[9] - i * 10) + "dbm", {
				position : new BMap.Point(point.lng, point.lat + ((d) / (2 * Math.PI * 6378137)) * 360),
				offset : new BMap.Size(5, -10)
			});
			label.setStyle({
				color : "yellow",
				backgroundColor : "gray"
			});
			map.addOverlay(label);

		}
	}
	function addClickHandler4(content, marker) {
		marker.addEventListener("click", function(e) {
			openInfo4(content, e);
		});
	}
	function openInfo4(content, e) {
		var p = e.target;
		var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
		var infoWindow = new BMap.InfoWindow(
				content,
				{
					width : 300,
					height : 300,
					title : "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;台站登记属性"
				});
		map.openInfoWindow(infoWindow, point);
		
   }
/************************************************************************************************************************/ 
/********************************************4.登记发射台站的位置及属性显示图显示函数*******************************************/    
  //map.clearOverlays();
     /*
     没有加 64 功能妈
     
     var content = 
          "<br>"+"归属单位："+array[1]
           +"<br>"+"识别码："+array[2]
           +"<br>"+"地理位置："+array[3]+","+array[4]+","+array[5]
           +"<br>"+"中心频率许可范围："+array[6]+"-"+array[7]
           +"<br>"+"额定发射最大功率："+array[8]
           +"<br>"+"信号工作带宽："+array[9]
           +"<br>"+"调制方式："+array[10]
           +"<br>"+"调制参数："+array[11]
           +"<br>"+"业务属性："+array[12]
           +"<br>"+"标称覆盖半径："+array[13]
           +"<br>"+"时间占用度："+array[14];
       */    
           
    var markerClustere;
function index4_go(array) {
       		
       		map.centerAndZoom(new BMap.Point(114.420239, 30.515488), 16); ////////////
       		
       		function index4_1_go(){
       			
       		if(markerClustere!=null)
       		markerClustere.clearMarkers();
       		//当前页面不是该服务的时候移除对地图的绑定。
       		if((document.getElementById ('select1').value!=4 )&&(document.getElementById ('select1').value!=6) )

            {map.removeEventListener("dragend",index4_1_go);return;}
       		
       		var point;
       		var marker;
       		var myIcon;
       		var markers = [];
       		for (var i = 0; i < array.length/14; i++) {
       		    point = new BMap.Point(parseFloat(array[14*i+2]) + 0.012,parseFloat(array[14*i+3]) + 0.003745);
       			
       			if(map.getBounds().containsPoint(point)){//如果改点再当前可视范围，则显示。2016-04-27 17:00新增 
       				
       				 if( array[14*i]===("chinaNet") ){
       			            myIcon = new BMap.Icon("imgs/dianxin1.png",new BMap.Size(40, 50));
       					}else if( array[14*i]===("chinaMove") ){
       						myIcon = new BMap.Icon("imgs/yidong1.png",new BMap.Size(40, 50));
       					}else if( array[14*i]===("chinaUnion") ){
       						myIcon = new BMap.Icon("imgs/liantong1.png",new BMap.Size(40, 50));
       					}else{
       				        myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png",new BMap.Size(23, 25));
       				    }
       		    marker = new BMap.Marker(point, {icon : myIcon});
       		    //marker = new BMap.Marker(point);
       			markers.push(marker);
       		
       			var content = "<br>" + "归属单位：" + array[14*i] + "<br>"
       					+ "地理位置："
       					+ array[14*i+2] + "<br>" + array[14*i+3] + "<br>"
       					+ array[14*i+4] + "<br>" + "中心频率许可范围："
       					+ array[14*i+5] + "-" + array[14*i+6] + "<br>"
       					+ "额定发射最大功率：" + array[14*i+7] + "<br>" + "信号工作带宽："
       					+ array[14*i+8] + "<br>" + "调制方式："
       					+ array[14*i+9] + "<br>" + "调制参数："
       					+ array[14*i+10] + "<br>" + "业务属性："
       					+ array[14*i+11] + "<br>" + "标称覆盖半径："
       					+ array[14*i+12] + "<br>" + "时间占用度："
       					+ array[14*i+13];
       			addClickHandler(content,marker);////////
       		  }
       		}
       	    markerClustere = new BMapLib.MarkerClusterer(map, {'markers':markers});
       	}	
       		index4_1_go();
       	    map.addEventListener("dragend",index4_1_go);
       	}
       	   
       	function addClickHandler(content, marker) {/////////
       		marker.addEventListener("click", function(e) {
       			openInfo(content, e);
       		});
       	}
       	function openInfo(content, e) {
       		var p = e.target;
       		var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
       		var infoWindow = new BMap.InfoWindow(
       				content,
       				{
       					width : 300,
       					height : 300,
       					title : "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;台站登记属性"
       				});
       		map.openInfoWindow(infoWindow, point);
       	}

/************************************************************************************************************************/
/********************************************5.登记发射台站的当前位置及等功率覆盖圆图显示函数*******************************************/    
function index5_go(array){
    //map.clearOverlays();
    
    var point = new BMap.Point(array[3]*1,array[4]*1);
    map.centerAndZoom(new BMap.Point(114.420239,30.515488),13);////////////

  var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png", new BMap.Size(23, 25),{offset: new BMap.Size(10, 25),imageOffset: new BMap.Size(0, 0-4*25)}); 
    var marker = new BMap.Marker(point, {icon: myIcon});
  
    map.addOverlay(marker);
    var content =                  
       "<br>"+"归属单位："+array[1]
        +"<br>"+"识别码："+array[2]
        +"<br>"+"地理位置："+array[3]+","+array[4]+","+array[5]
        +"<br>"+"中心频率："+array[6]
        +"<br>"+"额定发射最大功率："+array[7]
        +"<br>"+"衰减指数："+array[8]
        +"<br>"+"信号工作带宽："+array[9]
        +"<br>"+"调制方式："+array[10]
        +"<br>"+"调制参数："+array[11]
        +"<br>"+"业务属性："+array[12]
        +"<br>"+"活跃度："+array[13]
        +"<br>"+"是否非法："+array[14];
    addClickHandler5(content,marker);
  //marker.setAnimation(BMAP_ANIMATION_BOUNCE);
  var strokeColors =["#960000","#FD2D00","#FFb600","#FFD600","#7FFE7D","#02CEFF","#aabbcc"];
  var d=0;
  for(var i=0;i<strokeColors.length;i++){
    
  d=Math.sqrt( Math.pow( 10,10*i/(5*2) ) );//每10dbm一个圆
    
    var circle = new BMap.Circle(point,d,{strokeColor:strokeColors[i],fillColor:"",strokeWeight:3, strokeStyle:"", strokeOpacity:0.8});
    map.addOverlay(circle);//增加圆
    circle.addEventListener("click",function(e){alert("功率值:"+e.target.getStrokeColor());});
    
    var label = new BMap.Label("功率值:"+(array[7]-i*10)+"dbm",{position:new BMap.Point(point.lng,point.lat+((d)/(2*Math.PI*6378137))*360),offset:new BMap.Size(5,-10)});
    label.setStyle({ color : "blue",backgroundColor:"gray"});
    map.addOverlay(label);
  
  }
}
function addClickHandler5(content,marker){
 marker.addEventListener("click",function(e){openInfo5(content,e);});
}
function openInfo5(content,e){
var p = e.target;
var point = new BMap.Point(p.getPosition().lng,p.getPosition().lat);
var infoWindow = new BMap.InfoWindow(content,{width:300,height:300,title:"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;台站登记属性"});
map.openInfoWindow(infoWindow,point);
}
/************************************************************************************************************************/     
/********************************************6.所有发射台站的位置及属性显示图显示函数*******************************************/    
function index6_go(array){
  map.clearOverlays();
   var points =[];
   var len = (array.length-1)/2;
   var n=0;
   for(var i=1;i<=len;i++){
     points.push(new BMap.Point(array[2*i-1]*1, array[2*i]*1));//将返回的数据解析解析成点的数组
     var marker = new BMap.Marker(points[i-1]);
     map.addOverlay(marker);
     var content = 
          "<br>"+"归属单位："
           +"<br>"+"识别码："
           +"<br>"+"地理位置："+array[2*i-1]*1+","+array[2*i]*1
           +"<br>"+"中心频率许可范围："
           +"<br>"+"额定发射最大功率："
           +"<br>"+"信号工作带宽："
           +"<br>"+"调制方式："
           +"<br>"+"调制参数："
           +"<br>"+"业务属性："
           +"<br>"+"标称覆盖半径："
           +"<br>"+"时间占用度：";
     addClickHandler1(content,marker);
   }
   map.centerAndZoom(new BMap.Point(114.420239,30.515488),13); ////////////
}
function addClickHandler1(content,marker){
   marker.addEventListener("click",function(e){openInfo1(content,e);});
}
function openInfo1(content,e){
    var p = e.target;
    var point = new BMap.Point(p.getPosition().lng,p.getPosition().lat);
    var infoWindow = new BMap.InfoWindow(content,{width:300,height:300,title:"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;全部台站记录属性"});
    map.openInfoWindow(infoWindow,point); 
}
/********************************************7.所有注册监测终端的位置及属性显示图显示函数*******************************************/    
/************************************************************************************************************************/     
function index7_go(array){
  //map.clearOverlays();
   var point = new BMap.Point(array[3]*1, array[4]*1);
   map.centerAndZoom(new BMap.Point(114.420239,30.515488),13); ////////////
   //var n=0;

     var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png", new BMap.Size(23, 25),{offset: new BMap.Size(10, 25),imageOffset: new BMap.Size(0, 0-6*25)}); 
       var marker = new BMap.Marker(point, {icon: myIcon});
     map.addOverlay(marker);
     var content = 
          "<br>"+"终端ID号："+array[1]
           +"<br>"+"终端类型："+array[2]
           +"<br>"+"地理位置："+array[3]+","+array[4]+","+array[5]
            +"<br>"+"注册时间："+array[6]
           +"<br>"+"最近一次登陆时间："+array[7];

   addClickHandler2(content,marker);
}
function addClickHandler2(content,marker){
   marker.addEventListener("click",function(e){openInfo2(content,e);});
}
function openInfo2(content,e){
    var p = e.target;
    var point = new BMap.Point(p.getPosition().lng,p.getPosition().lat);
    var infoWindow = new BMap.InfoWindow(content,{width:200,height:250,title:"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所有注册终端属性"});
    map.openInfoWindow(infoWindow,point); 
}

/************************************************************************************************************************/     
/********************************************8.当前所有在网监测终端的位置及属性图显示函数*******************************************/    
function index8_go(array){
  //map.clearOverlays();
   var point = new BMap.Point(array[3]*1, array[4]*1);
   map.centerAndZoom(new BMap.Point(114.420239,30.515488),13); ////////////
   //var n=0;

     var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png", new BMap.Size(23, 25),{offset: new BMap.Size(10, 25),imageOffset: new BMap.Size(0, 0-6*25)}); 
       var marker = new BMap.Marker(point, {icon: myIcon});
     map.addOverlay(marker);
     var content = 
          "<br>"+"终端ID号："+array[1]
           +"<br>"+"终端类型："+array[2]
           +"<br>"+"地理位置："+array[3]+","+array[4]+","+array[5]
           +"<br>"+"注册时间："+array[6]
           +"<br>"+"最近一次登陆时间："+array[7];

   addClickHandler3(content,marker);
   
   var t1=0; t2=0;
   t1=window.setInterval(function(){
	   if(t2==0){
		   t2=1;
		   marker.show();
		   }
		   else {
			   t2=0;
			   marker.hide();
		   }
	   
   },200);
   
     map.addEventListener("click",function(){window.clearInterval(t1);                    
                                            marker.show();
                                            t1=t2=0;});     
}
function addClickHandler3(content,marker){
   marker.addEventListener("click",function(e){openInfo3(content,e);});
}
function openInfo3(content, e) {
	var p = e.target;
	var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
	var infoWindow = new BMap.InfoWindow(
			content,
			{
				width : 200,
				height : 250,
				title : "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;所有在网终端属性"
			});
	map.openInfoWindow(infoWindow, point); }

/************************************************************************************************************************/     


/**********************************9. 本地的功率谱数据文件 路径 图 ******************************************************/     
TIME1=0,TIME2=0;
function alwaysSendData(){
	
	var obj= document.getElementById("select1");
    var index = obj.selectedIndex; // 选中索引
    var value= obj.options[index].value;
    
     if(value=="9"){
          
	
	
	       if(TIME2==1){
		       TIME2=0;
	           document.getElementById("genzong").value = "跟踪";
	           window.clearInterval(TIME1);
	           TIME1 = 0;
	       }
	       else{ 
	    	   map.clearOverlays();
	    	   
		       TIME2=1;
		       document.getElementById("genzong").value = "关闭";
		       TIME1 = window.setInterval(function(){   
			     
	           $.post("http://localhost:8080/MapTest/QueryDataBase", 
   	            {
   				     convertData:""+9  //将页面设置的地图服务参数传到服务器
                 
   			    },
   		        function(responseData,status)
   		        {    
   				     //requestData.splice(0,requestData.length);//每次发完请求数据后就清除请求数据缓冲数组
   				     //alert("响应数据：\n"+responseData);

   		             if(status==="success" && responseData!="")
   		             {//如果回传数据成功 
   		           // 	alert("响应数据：\n"+responseData);
   		       
   		             // map.clearOverlays();
                     
   		             var len = responseData.split("|").length;
                     var responseDataArray1 = new Array();//响应数组
                     var responseDataArray2 = new Array();//响应数组
                   responseDataArray1 = responseData.split("|");
            
                   for(var i=0;i<len;i++){
                       responseDataArray2.push(responseDataArray1[i].split(",")[1]);// longitude////
                       responseDataArray2.push(responseDataArray1[i].split(",")[2]);// latitude////
                          }
                     
                     index9_go(responseDataArray2);
                     
	                 responseDataArray2.splice(0,responseDataArray2.length);
	                 }
	                
   		             });
   		       },3000);
	     }
		      
     }
}
function index9_go(array){
	
 
   
   //map.centerAndZoom(new BMap.Point(114.420239, 30.515488), 19);
  map.centerAndZoom(new BMap.Point(1 * parseFloat(array[0]) + 0.012,1 *parseFloat( array[1]) + 0.003745),19);

	var len = array.length/2;
	var points = [];

	for (var i = 0; i < len; i++) {
		//points.push(new BMap.Point(1*array[i].LONGITUDE+0.01217, 1*array[i].LATITUDE+0.0118));//将返回的数据解析解析成点的数组
		points.push(new BMap.Point(1 * parseFloat(array[2*i]) + 0.012,1 *parseFloat( array[2*i+1]) + 0.003745));//将返回的数据解析解析成点的数组

	}
	var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png",
			new BMap.Size(23, 25), {
				offset : new BMap.Size(10, 25),
				imageOffset : new BMap.Size(0, 0 - 0 * 25)
			});
	map.addOverlay(new BMap.Marker(points[0], {
		icon : myIcon
	}));
	

  //  map.centerAndZoom(points[0],15);
		//添加远点到地图 


		//添加折线到地图上
		var polyline = new BMap.Polyline(points, {strokeColor:"blue", strokeWeight:5, strokeOpacity:0.6});
		map.addOverlay(polyline);
	


}

</script>
</html>