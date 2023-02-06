"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_read_counter(self):
        """It should read the counter"""
        result = self.client.post("/counters/aa")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # read the counter
        result = self.client.get("/counters/aa")
        read = result.get_json()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(read['aa'],0)

    def test_read_counter_cannot_find(self):
        """Read a counter that cannot find - return 404"""
        result = self.client.get("/counters/bb")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_counter(self):
        """Detele a counter """
        result = self.client.post("/counters/bb")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # delete the counter
        result = self.client.delete("/counters/bb")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_counter_cannot_find(self):
        """Detele a counter that cannot find - return 404"""
        result = self.client.delete("/counters/bb")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_counter(self):
        """It should update the counter"""
        self.client.delete("/counters/aa")
        result = self.client.post("/counters/aa")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        baseline = data['aa']
        result = self.client.put("/counters/aa")
        update = result.get_json()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(baseline+1,update['aa'])

    def test_update_counter_cannot_find(self):
        """Update a counter that cannot find - return 404"""
        result = self.client.put("/counters/bb")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
