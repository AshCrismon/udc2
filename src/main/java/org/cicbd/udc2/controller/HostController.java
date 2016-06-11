package org.cicbd.udc2.controller;

import java.util.Map;

import org.cicbd.udc2.service.HostMetricService;
import org.cicbd.udc2.vo.MetricVo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/metric")
public class HostController {
	
	@Autowired
	private HostMetricService<MetricVo> hostMetricService;
	
	@RequestMapping(value = "/{hostname}/{metricName}", method = RequestMethod.GET)
	public Map<String, Object> findMetricData(
			@PathVariable String hostname, 
			@PathVariable String metricName, 
			long beginTime, long endTime){
		return hostMetricService.findMetricData(hostname, metricName, beginTime, endTime);
	}
}
