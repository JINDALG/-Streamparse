(ns Motion_Detection
	(:use	[streamparse.specs])
	(:gen-class))
(defn Motion_Detection [options]
	[
	;; spout configuration
	{"Motion-Spout" (python-spout-spec
		options
		"spouts.Motion_Spout.Motion_Spout"
		["URL"]
		)
	}
	;; bolt configuration
	{"Motion-Frame" (python-bolt-spec
		options
		{"Motion-Spout" :shuffle}
		"bolts.Motion_Frame.Motion_Frame"
		["a" "x"]
		:p 2
		)
	
	;; bolt configuration
	"Motion-Bolt" (python-bolt-spec
		options
		{"Motion-Frame" :shuffle}
		"bolts.Motion_Bolt.Motion_Bolt"
		["z" "sID"]
		:p 2
		)
	}
	]
)
