package org.cicbd.udc2.repository;

import java.util.List;

import org.cicbd.udc2.model.MetricData;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class MetricDataRepository extends CommonRepository<MetricData> {
	
	/**
	 * fetch the metric data from the specified collection according to the query string 
	 * such as "{metric: 'cpu_aidle', clock: {$gte: beginTime, $lte: endTime}}", and
	 * return the specified fields
	 * @param collectionName
	 * @param query
	 * @param fields
	 * @return
	 */
	List<MetricData> findMetricData(String collectionName, String queryStr, String fields){
		validateCollection(collectionName);
		Query basicQuery = new BasicQuery(queryStr, fields).with(new Sort(Direction.DESC, "clock"));
		return find(basicQuery, collectionName);
	};
	
	/**
	 * fetch the metric data from the specified collection according to the query string 
	 * such as "{metric: 'cpu_aidle', clock: {$gte: beginTime, $lte: endTime}}"
	 * @param collectionName
	 * @param query
	 * @return
	 */
	public List<MetricData> findMetricData(String collectionName, String queryStr) {
		validateCollection(collectionName);
		Query basicQuery = new BasicQuery(queryStr).with(new Sort(Direction.DESC, "clock"));
		return find(basicQuery, collectionName);
	}
	
	/**
	 * fetch the metric data from the specified collection, 
	 * the time range of the metric data is also specified
	 * @param collectionName
	 * @param metricName
	 * @param beginTime
	 * @param endTime
	 * @return
	 */
	public List<MetricData> findMetricData(String collectionName, String metricName, long beginTime, long endTime){
		validateCollection(collectionName);
		StringBuilder queryStr = new StringBuilder();
		queryStr.append("{metric: '" + metricName + "'");
		queryStr.append(", clock: {$gte: '" + beginTime + "', $lte: '" + endTime + "'}}");
		String fields = "{id: 0, metric: 0}";
		return findMetricData(collectionName, queryStr.toString(), fields);
	}
	
}
