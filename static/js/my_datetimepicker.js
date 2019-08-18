        $(function() {
			$('#datetimepicker').datetimepicker();
			$(".form-control").datetimepicker({
				format : 'yyyy-mm-dd', // 展现格式
				startDate : "1980-01-01",// 开始时间
				//endDate : "2020-01-01", // 结束时间
				autoclose : true, // 选择日期后关闭
				// 选择器打开之后首先显示的视图
				// 0表示分钟(默认),1表示小时,2表示天,3表示月,4表示年
				startView : 2,
				// 选择器所能够提供的最精确的时间选择视图
				// 0表示分钟(默认),1表示小时,2表示天,3表示月,4表示年
				minView : 2,
				language : 'zh-CN', //显示语言为中文
			});

		});