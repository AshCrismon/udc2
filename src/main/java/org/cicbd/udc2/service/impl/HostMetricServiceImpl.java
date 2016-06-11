package org.cicbd.udc2.service.impl;

import java.util.List;
import java.util.Map;

import org.cicbd.udc2.exception.CollectionNotFoundException;
import org.cicbd.udc2.helper.HostDataSinker;
import org.cicbd.udc2.service.HostMetricService;
import org.cicbd.udc2.vo.MetricVo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class HostMetricServiceImpl implements HostMetricService<MetricVo> {

	@Autowired
	private MongoTemplate mongo;
	
	@Override
	public List<MetricVo> findMetricData(String collectionName, String query, String fields) {
		if(!mongo.collectionExists(collectionName)){
			throw new CollectionNotFoundException(collectionName);
		}
		Query basicQuery = null;
		if(StringUtils.isEmpty(fields)){
			basicQuery = new BasicQuery(query).with(new Sort(Direction.DESC, "timestamp"));
		}else{
			basicQuery = new BasicQuery(query, fields).with(new Sort(Direction.DESC, "timestamp"));
		}
		return mongo.find(basicQuery, MetricVo.class, collectionName);
	}
	
	@Override
	public List<MetricVo> findMetricData(String collectionName, String query) {
		return findMetricData(collectionName, query, null);
	}
	
	@Override
	public Map<String, Object> findMetricData(String collectionName, String metricName, long beginTime, long endTime){
		StringBuilder query = new StringBuilder("");
		query.append("{metric: '" + metricName + "'");
		query.append(", timestamp: {$gte: " + beginTime + ", $lte: " + endTime + "}}");
		String fields = "{id: 0, metric: 0}";
		return HostDataSinker.sink(collectionName, metricName, findMetricData(collectionName, query.toString(), fields));
	}

}
