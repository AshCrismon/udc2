package org.cicbd.udc2.repository;

import org.cicbd.udc2.model.HostInfo;
import org.springframework.data.mongodb.core.query.BasicQuery;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class HostInfoRepository extends CommonRepository<HostInfo> {

	private final static String COLLECTION_NAME = "host_info";
	
	public HostInfo findHostInfoByQuery(String queryStr, String fields){
		validateCollection(COLLECTION_NAME);
		Query basicQuery = new BasicQuery(queryStr, fields);
		return findOne(basicQuery, COLLECTION_NAME);
	}
	
	public HostInfo findHostInfoByQuery(String queryStr){
		validateCollection(COLLECTION_NAME);
		Query basicQuery = new BasicQuery(queryStr);
		return findOne(basicQuery, COLLECTION_NAME);
	}
	
	public HostInfo findHostInfo(String hid){
		validateCollection(COLLECTION_NAME);
		StringBuilder queryStr = new StringBuilder();
		queryStr.append("{hid: '" + hid + "'}");
		return findHostInfoByQuery(queryStr.toString());
	}
}
