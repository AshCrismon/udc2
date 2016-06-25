package org.cicbd.udc2.service.impl;

import java.util.List;
import java.util.Map;

import org.cicbd.udc2.helper.MetricAdaptor;
import org.cicbd.udc2.model.MetricData;
import org.cicbd.udc2.model.MetricInfo;
import org.cicbd.udc2.repository.MetricDataRepository;
import org.cicbd.udc2.repository.MetricInfoRepository;
import org.cicbd.udc2.service.MetricService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MetricServiceImpl implements MetricService{

	@Autowired
	private MetricDataRepository metricDataRepository;
	@Autowired
	private MetricInfoRepository metricInfoRepository;
	
	public Map<String, Object> findMetric(String mid, long beginTime, long endTime){
		String collectionName = mid.substring(0, mid.lastIndexOf("/"));
		String metricName = mid.substring(mid.lastIndexOf("/") + 1);
		List<MetricData> metricData = metricDataRepository.findMetricData(collectionName, metricName, beginTime, endTime);
		MetricInfo metricInfo = metricInfoRepository.findMetricInfo(mid);
		return MetricAdaptor.adapt(collectionName, metricName, metricData, metricInfo);
	}
	
	public Map<String, Object> findMetric(String cid, String metricName, long beginTime, long endTime){
		List<MetricData> metricData = metricDataRepository.findMetricData(cid, metricName, beginTime, endTime);
		MetricInfo metricInfo = metricInfoRepository.findMetricInfo(cid + "/" + metricName);
		return MetricAdaptor.adapt(cid, metricName, metricData, metricInfo);
	}
}
