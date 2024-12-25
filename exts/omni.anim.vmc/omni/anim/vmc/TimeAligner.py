import time

class TimeAligner:
    def __init__(self):
        self.initialized = False  # Flag to check if TimeAligner is initialized
        self.time_offset = 0  # The offset between real-world time and the first timestamp

    def reset(self):
        self.initialized = False

    def initialize(self, timestamp):
        """Initialize alignment with the first frame's timestamp."""
        if not self.initialized:
            start_time = time.time()
            self.time_offset = start_time - timestamp  # Calculate offset
            self.initialized = True  # Mark as initialized

    def align_time(self):
        """Return the current aligned time based on the offset."""
        if not self.initialized:
            return None  # Not initialized yet
        return time.time() - self.time_offset  # Return aligned current 

    def get_valid_frame(self, frame_queue):
        """
        Get the first valid frame from the queue based on the current aligned time.
        
        Args:
            frame_queue (list): A list of frames, each containing a 'timestamp' key.
        
        Returns:
            dict or None: The first valid frame whose timestamp is not outdated, or None if no valid frame exists.
        """
        # Initialize alignment with the first frame's timestamp if not already done
        if not self.initialized and not frame_queue.is_empty():
            front_frame = frame_queue.front()  # Peek at the front frame without removing it
            self.initialize(front_frame['timestamp'])  # Initialize with first frame's timestamp
            return front_frame

        current_aligned_time = self.align_time()  # Get aligned current time
        if current_aligned_time is None:
            return None  # Not initialized yet
        
        # While there are frames in the queue and the front frame's timestamp is less than or equal to current time
        while frame_queue and not frame_queue.is_empty():
            front_frame = frame_queue.front()  # Peek at the front frame without removing it
            if front_frame['timestamp'] >= current_aligned_time:
                print(f"Dequeue timestamp: {front_frame['timestamp']}")
                return front_frame  # Return the first valid future frame
            
            frame_queue.dequeue()  # Remove outdated frames

        return None  # No valid frames found