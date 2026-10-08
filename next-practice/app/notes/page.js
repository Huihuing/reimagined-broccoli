import Notes from "../../components/Notes";

export const metadata = { title: "메모 | Little Notes" };

export default function NotesPage() {
  return (
    <div className="notes-page">
      <div className="notes-heading">
        <div><span className="eyebrow">YOUR PERSONAL SPACE</span><h1>나의 메모<span className="accent-dot">.</span></h1><p>떠오르는 생각을 놓치지 마세요. 작성한 내용은 이 브라우저의 현재 세션에만 남습니다.</p></div>
        <span className="pill">✳ IN MEMORY</span>
      </div>
      <Notes />
    </div>
  );
}
