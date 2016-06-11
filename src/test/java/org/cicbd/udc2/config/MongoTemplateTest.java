package org.cicbd.udc2.config;

import org.junit.Before;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import static org.junit.Assert.*;

public class MongoTemplateTest extends AbstractTestConfig{

	@Autowired
	private MongoTemplate mongo;
	
	@Before
	public void before(){
		assertNotNull(mongo);
	}
	
	@Test
	public void testDBName(){
		assertEquals("udc2_ganglia", mongo.getDb().getName());
	}
	
	@Test
	public void testCreateCollection(){
		mongo.createCollection("testCollection");
		assertTrue(mongo.collectionExists("testCollection"));
	}
	
	@Test
	public void testDeleteCollection(){
		mongo.dropCollection("testCollection");
		assertTrue(!mongo.collectionExists("testCollection"));
	}
	
}
