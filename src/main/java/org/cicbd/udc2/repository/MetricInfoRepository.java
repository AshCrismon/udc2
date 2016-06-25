package org.cicbd.udc2.repository;

import org.cicbd.udc2.model.MetricInfo;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class MetricInfoRepository  extends CommonRepository<MetricInfo>{
	
	private final static String COLLECTION_NAME = "metric_info";
	
	public MetricInfo findMetricInfoByQuery(String queryStr, String fields){
		validateCollection(COLLECTION_NAME);
		Query basicQuery = new BasicQuery(queryStr, fields);
		return findOne(basicQuery, COLLECTION_NAME);
	}
	
	public MetricInfo findMetricInfoByQuery(String queryStr){
		validateCollection(COLLECTION_NAME);
		Query basicQuery = new BasicQuery(queryStr);
		return findOne(basicQuery, COLLECTION_NAME);
	}
	
	public MetricInfo findMetricInfo(String mid){
		validateCollection(COLLECTION_NAME);
		StringBuilder queryStr = new StringBuilder();
		queryStr.append("{mid: '" + mid + "'}");
		return findMetricInfoByQuery(queryStr.toString());
	}
}
