package org.cicbd.udc2.controller;

import java.util.Map;

import org.cicbd.udc2.service.MetricService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/metric")
public class MetricController {
	
	@Autowired
	private MetricService metricService;
	
	@RequestMapping(value = "/{metricName}", method = RequestMethod.GET)
	public Map<String, Object> findMetricData(
			@PathVariable String metricName, 
			String cid, 
			long beginTime, 
			long endTime){
		return metricService.findMetric(cid, metricName, beginTime, endTime);
	}
}
