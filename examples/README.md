<a href="https://www.ultralytics.com" target="_blank"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Ultralytics YOLO Examples

These community-contributed examples focus on tracking and related applications
retained in this fork. Each example can require optional packages, models, or
specific hardware; check its own instructions before running it.

## Python Examples

| Example | Purpose |
| --- | --- |
| [Axelera pose tracking](./YOLO-Axelera-Python) | YOLO26 pose inference with optional Axelera tracking. |
| [Interactive tracking UI](./YOLO-Interactive-Tracking-UI) | Select and follow objects in an OpenCV interface. |
| [Action recognition](./YOLOv8-Action-Recognition) | Track people and classify actions in video. |
| [Region counter](./YOLOv8-Region-Counter) | Count tracked objects in adjustable regions. |

## Notebooks

| Notebook | Purpose |
| --- | --- |
| [Object tracking](./object_tracking.ipynb) | Track objects across video frames. |
| [Object counting](./object_counting.ipynb) | Count tracked objects. |
| [Heatmaps](./heatmaps.ipynb) | Visualize object movement over time. |

## External Examples

### C# / .NET

| Title                                                                              | Backend      | Contributor                                     |
| ---------------------------------------------------------------------------------- | ------------ | ----------------------------------------------- |
| [YOLO C# ONNX Runtime (YoloSharp)](https://github.com/dme-compunet/YoloSharp)      | ONNX Runtime | [Compunet](https://github.com/dme-compunet)     |
| [YOLO .NET ONNX Detection (Yolov8.Net)](https://www.nuget.org/packages/Yolov8.Net) | ONNX         | [Samuel Stainback](https://github.com/sstainba) |
| [RTDETR ONNX Runtime C#](https://github.com/Kayzwer/yolo-cs/blob/master/RTDETR.cs) | ONNX Runtime | [Kayzwer](https://github.com/Kayzwer)           |

## 🤝 How to Contribute

We actively encourage contributions from our vibrant community! Sharing your examples, applications, and guides helps others learn and build amazing things with [Ultralytics](https://www.ultralytics.com). If you have a project you'd like to share, please follow these steps:

1.  **Fork the Repository:** Start by forking the main [Ultralytics repository](https://github.com/ultralytics/ultralytics) on [GitHub](https://github.com/).
2.  **Create Your Example:** Add your project folder within the `examples/` directory of your forked repository.
3.  **Prepare Your Submission:** Ensure your project meets the following criteria:
    - It utilizes the `ultralytics` pip package.
    - Includes a `README.md` file with clear, step-by-step instructions for setup and execution. Explain the purpose of the example and any prerequisites.
    - Avoid committing large files or extensive dependencies. If necessary, provide instructions for users to download them separately (e.g., using `ultralytics.utils.downloads.safe_download()`).
    - As a contributor, be prepared to offer support and address [issues](https://github.com/ultralytics/ultralytics/issues) related to your example.
4.  **Submit a Pull Request:** Create a [pull request (PR)](https://github.com/ultralytics/ultralytics/pulls) targeting the `main` branch of the official Ultralytics repository. Use the title prefix `[Example]` (e.g., `[Example] Add YOLO26 Pose Estimation on Raspberry Pi`).

For more comprehensive guidelines on contributing code, documentation, or examples, please refer to our [Contributing Guide](https://docs.ultralytics.com/help/contributing). We appreciate your efforts to enhance the Ultralytics ecosystem! If you have questions, feel free to open an issue or PR, and the team will be happy to assist. Check out the [Ultralytics Blog](https://www.ultralytics.com/blog) for more insights and updates, and explore [Ultralytics Platform](https://platform.ultralytics.com/ultralytics/yolo26) for streamlined model training and deployment.
