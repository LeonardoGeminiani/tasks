### Example in waybar config:

```json
"custom/tasks" : {
    "format": "{}",
    "return-type": "json",
    "exec":  "~/.config/tasks_waybar/waybar_GetCurrentTask.py",
    "restart-interval": 2
  },
```