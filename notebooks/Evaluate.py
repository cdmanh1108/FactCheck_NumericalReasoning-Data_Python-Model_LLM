import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
warnings.filterwarnings('ignore')

# ===== TẢI DỮ LIỆU =====
project_root = Path(__file__).parent.parent
results_path = project_root / "data" / "processed" / "finetuned_results.csv"

if not results_path.exists():
    raise FileNotFoundError(
        f"Chưa có file kết quả dự đoán!\n"
        f"Hãy chạy Inference trên Google Colab trước, "
        f"sau đó tải file finetuned_results.csv về đặt tại:\n{results_path}"
    )

df_test = pd.read_csv(results_path)
print(f"✅ Đã tải {len(df_test)} dòng kết quả dự đoán!")

# ===== ĐÁNH GIÁ MÔ HÌNH =====
valid_idx = df_test['Predicted_Label'] != -1

if valid_idx.sum() == 0:
    print("❌ Tất cả dự đoán đều bị lỗi rác! Cần kiểm tra lại model.")
else:
    y_true = df_test.loc[valid_idx, 'labels'].astype(int)
    y_pred = df_test.loc[valid_idx, 'Predicted_Label'].astype(int)

    # 1. IN BẢNG ĐIỂM DẠNG TEXT
    print("\n" + "🔥" * 25)
    print(" 🏆 BẢNG ĐIỂM CỦA MÔ HÌNH AI SAU KHI TRAIN")
    print("🔥" * 25)

    acc        = accuracy_score(y_true, y_pred)
    f1_macro   = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')

    print(f"🎯 Độ chính xác (Accuracy)  : {acc * 100:>6.2f} %")
    print(f"⚖️ Điểm cân bằng (Macro F1) : {f1_macro * 100:>6.2f} %")
    print(f"📦 Điểm F1 có trọng số      : {f1_weighted * 100:>6.2f} %")
    print("-" * 50)
    print("📋 BÁO CÁO CHI TIẾT TỪNG NHÃN:")
    print("   (0: Hỗ trợ, 1: Bác bỏ, 2: Thiếu Thông Tin)\n")
    print(classification_report(y_true, y_pred, digits=4, zero_division=0))

    loi = len(df_test) - valid_idx.sum()
    if loi > 0:
        print(f"\n⚠️ LƯU Ý: Có {loi} câu AI bị nhầm lẫn (ảo giác) và không nhả ra số hợp lệ.")
    print("=" * 50)

    # 2. VẼ MA TRẬN NHẦM LẪN (CONFUSION MATRIX)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['0 (Support)', '1 (Refute)', '2 (NEI)'],
                yticklabels=['0 (Support)', '1 (Refute)', '2 (NEI)'],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title('MA TRẬN NHẦM LẪN (CONFUSION MATRIX)', fontweight='bold', pad=15)
    plt.ylabel('Đáp Án Chuẩn (Thực tế)', fontweight='bold')
    plt.xlabel('AI Dự Đoán', fontweight='bold')
    plt.tight_layout()
    plt.savefig(project_root / "notebooks" / "confusion_matrix.png", dpi=150)
    plt.show()
    print("💾 Đã lưu biểu đồ tại: notebooks/confusion_matrix.png")
