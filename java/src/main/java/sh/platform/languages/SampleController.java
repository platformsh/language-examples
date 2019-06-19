package sh.platform.languages;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;
import java.util.stream.Stream;

import static java.util.stream.Collectors.toList;

@Controller
public class SampleController {

    @GetMapping("java")
    public String getStatus(Model model) {
        List<SampleCodeStatus> codes = Stream.of(SampleCodeType.values())
                .map(SampleCodeStatus::of)
                .sorted()
                .collect(toList());
        model.addAttribute("codes", codes);
        return "index";
    }

}
